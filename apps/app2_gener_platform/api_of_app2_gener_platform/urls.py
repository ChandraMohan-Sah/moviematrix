# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('genrelist', views.GenreCreateList.as_view(), name="genre-list-create"),
    path('genredetail/<int:pk>/', views.GenreDetail.as_view(), name='genre-detail'),

    path('platformlist', views.PlatformListCreate.as_view(), name="platform-list-create"),
    path('platformdetail/<int:pk>/', views.PlatformDetail.as_view(), name="platform-detail")
]
