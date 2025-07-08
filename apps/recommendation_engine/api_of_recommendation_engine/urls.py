# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get_personalized_movie_recommendation/', views.get_personalized_movie_recommendation, name="get-personalized-movie-recommendation")
]
