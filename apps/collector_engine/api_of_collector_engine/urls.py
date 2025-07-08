# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get_popular_cast/', views.get_popular_cast, name='get_popular_cast'),
    path('get_popular_movies/', views.get_popular_movies, name="get-popular-movies"),
    path('get_fan_favourites/', views.get_fan_favourites, name="get-fan-favourites"),
    path('get_imdb_originals/', views.get_imdb_originals, name='get-imdb-originals'),
    path('get_prime_video/', views.get_prime_video, name="get-prime-video"),
    path('get_in_theaters/', views.get_in_theaters, name='get-in-theaters'),
    path('get_coming_soon_editors_pick/', views.get_coming_soon_editors_pick, name='get-coming-soon-editors-pick'),
    path('get_recently_viewed_movies/', views.get_recently_viewed_movies, name='get-recently-viewed-movies')
]
