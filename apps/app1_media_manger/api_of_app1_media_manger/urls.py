# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('mediafile_list/', views.MediaFileList.as_view(), name='mediafile-list'),
    # path('mediafile_detail/<int:pk>/', views.MediaFileDetail.as_view(), name='mediafile-detail'),

    #--------------------------------------------------------------------------------------------
    path('cast_create/create/', views.CastCreateView.as_view(), name='cast-create'),
    path('cast_rud/<int:pk>/', views.CastDetailView.as_view(), name='cast-rud'),

    #--------------------------------------------------------------------------------------------
    path('creator_create/create/', views.CreatorCreateView.as_view(), name='creator-create'),
    path('creator_rud/<int:pk>/', views.CreatorDetailView.as_view(), name='creator-rud'),

    #--------------------------------------------------------------------------------------------
    path('writer_create/create/', views.WriterCreateView.as_view(), name='writer-create'),
    path('writer_rud/<int:pk>/', views.WriterDetailView.as_view(), name='writer-rud'),

    #--------------------------------------------------------------------------------------------
    path('movie_create/create/', views.MovieCreateView.as_view(), name='movie-create'),
    path('movie_rud/<int:pk>/', views.MovieDetailView.as_view(), name='movie-rud'),

    #--------------------------------------------------------------------------------------------
    path('tvshow_create/create/', views.TVShowCreateView.as_view(), name='tvshow-create'),
    path('tvshow_rud/<int:pk>/', views.TVShowDetailView.as_view(), name='tvshow-rud'), 

    path('season_create/create/', views.SeasonCreateView.as_view(), name='season-create'),
    path('season_rud/<int:pk>/', views.SeasonDetailView.as_view(), name='season-rud'),    

    path('episode_create/create/', views.EpisodeCreateView.as_view(), name='episode-create'),
    path('episode_rud/<int:pk>/', views.EpisodeDetailView.as_view(), name='episode-rud'),
    #--------------------------------------------------------------------------------------------
]
