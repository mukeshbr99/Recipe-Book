from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Recipe, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-0',
                'placeholder': 'e.g., Dessert, Main Course, Vegan'
            })
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'category', 'ingredients', 'instructions', 'image', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-0',
                'placeholder': 'e.g., Spicy Garlic Pasta, Chocolate Cake, Greek Salad',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select bg-dark text-white border-0',
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-0',
                'rows': 4,
                'placeholder': 'Separate ingredients by commas\nExample: 400g Pasta, 6 cloves Garlic, 100ml Olive oil',
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-0',
                'rows': 6,
                'placeholder': 'Step-by-step cooking instructions\n1. Boil water in a large pot\n2. Add pasta and cook until al dente',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control bg-dark text-white border-0',
                'accept': 'image/*',
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class SignUpForm(forms.ModelForm):
    full_name = forms.CharField(max_length=150, label='Full Name')
    password = forms.CharField(widget=forms.PasswordInput, min_length=4)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', min_length=4)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        full_name = self.cleaned_data.get('full_name', '').strip()
        name_parts = full_name.split(' ', 1)
        user.first_name = name_parts[0] if name_parts else ''
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''

        # Use email as username fallback / uniqueness base
        base_username = self.cleaned_data.get('email', '').split('@')[0]
        username = base_username or 'user'
        existing = User.objects.filter(username=username).exists()
        counter = 1
        while existing:
            username = f"{base_username}{counter}"
            existing = User.objects.filter(username=username).exists()
            counter += 1
        user.username = username

        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class EmailAuthenticationBackend:
    """Custom backend that authenticates using email instead of username"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email__iexact=username)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-dark text-white border-0',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark text-white border-0',
            'placeholder': 'Enter your password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            self.user_cache = authenticate(username=email, password=password, backend=EmailAuthenticationBackend())
            if self.user_cache is None:
                raise forms.ValidationError('Invalid email or password.')
        return cleaned_data
    
    def get_user(self):
        return getattr(self, 'user_cache', None)
