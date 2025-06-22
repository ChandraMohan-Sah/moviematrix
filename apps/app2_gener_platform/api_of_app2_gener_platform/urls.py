# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('genrelist', views.GenreList.as_view(), name="genre-list"),
    path('genredetail/<int:pk>/', views.GenreDetail.as_view(), name='genre-detail'),

    path('platformlist', views.PlatformList.as_view(), name="platform-list"),
    path('platformdetail/<int:pk>/', views.PlatformDetail.as_view(), name="platform-detail")
]
