from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from .forms import LoginForm, RecipeForm, SignUpForm, CategoryForm
from .models import Category, Favorite, Like, Recipe


def home(request, slug=None):
    category = None
    recipes = Recipe.objects.select_related('category', 'author')

    query = request.GET.get('q', '')
    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(category__name__icontains=query)
        )

    if slug:
        category = get_object_or_404(Category, slug=slug)
        recipes = recipes.filter(category=category)

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recipes': page_obj,
        'categories': Category.objects.order_by('name'),
        'category': category,
        'query': query,
    }
    return render(request, 'home.html', context)


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    user_like = False
    user_favorite = False
    if request.user.is_authenticated:
        user_like = Like.objects.filter(user=request.user, recipe=recipe).exists()
        user_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()

    context = {
        'recipe': recipe,
        'user_like': user_like,
        'user_favorite': user_favorite,
    }
    return render(request, 'recipe_detail.html', context)


@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Recipe created successfully.')
            return redirect(recipe)
    else:
        form = RecipeForm()
    return render(request, 'recipe_form.html', recipe_form_context(form, 'Create'))


@login_required
def recipe_update(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        raise Http404
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated successfully.')
            return redirect(recipe)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipe_form.html', recipe_form_context(form, 'Update'))


@login_required
def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        raise Http404
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted.')
        return redirect('home')
    return render(request, 'recipe_confirm_delete.html', {'recipe': recipe})


def categories_list(request):
    categories = Category.objects.order_by('name')
    context = {
        'categories': categories,
    }
    return render(request, 'categories_list.html', context)


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('categories_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form, 'action': 'Create'})


@login_required
def ajax_like(request, recipe_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    like, created = Like.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': recipe.likes.count()})


@login_required
def ajax_favorite(request, recipe_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    fav, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        fav.delete()
        favorite = False
    else:
        favorite = True
    return JsonResponse({'favorite': favorite, 'favorites_count': recipe.favorites.count()})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def recipe_form_context(form, action):
    return {
        'form': form,
        'action': action,
        'form_fields': [
            (form['title'], '📝'),
            (form['category'], '🏷️'),
            (form['ingredients'], '🥘'),
            (form['instructions'], '👨‍🍳'),
            (form['image'], '📸'),
        ],
    }


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
