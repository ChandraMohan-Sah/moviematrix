# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users_movie_preferences/', views.users_movie_preferences, name="users-movie-preferences")
]
