from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.home, name='category'),
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/new/', views.recipe_create, name='recipe_create'),
    path('recipes/<slug:slug>/edit/', views.recipe_update, name='recipe_update'),
    path('recipes/<slug:slug>/delete/', views.recipe_delete, name='recipe_delete'),
    path('like/<int:recipe_id>/', views.ajax_like, name='ajax_like'),
    path('favorite/<int:recipe_id>/', views.ajax_favorite, name='ajax_favorite'),
    path('search/', views.home, name='search'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
