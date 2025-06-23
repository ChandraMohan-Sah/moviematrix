# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('mediafile_list/', views.MediaFileList.as_view(), name='mediafile-list'),
    # path('mediafile_detail/<int:pk>/', views.MediaFileDetail.as_view(), name='mediafile-detail'),

    #--------------------------------------------------------------------------------------------
    path('cast_media/list/', views.CastListView.as_view(), name='cast-media-list'),
    path('cast_media/create/', views.CastCreateView.as_view(), name='cast-media-create'),
    path('cast_rud/<int:pk>/', views.CastDetailView.as_view(), name='cast-media-rud'),

    #--------------------------------------------------------------------------------------------
    path('creator_media/list/', views.CreatorListView.as_view(), name='creator-media-list'),
    path('creator_media/create/', views.CreatorCreateView.as_view(), name='creator-media-create'),
    path('creator_rud/<int:pk>/', views.CreatorDetailView.as_view(), name='creator-media-rud'),

    #--------------------------------------------------------------------------------------------
    path('writer_media/list/', views.WriterListView.as_view(), name='writer-media-list'),
    path('writer_media/create/', views.WriterCreateView.as_view(), name='writer-media-create'),
    path('writer_media_rud/<int:pk>/', views.WriterDetailView.as_view(), name='writer-media-rud'),

    #--------------------------------------------------------------------------------------------
    path('movie_media/list/', views.MovieListView.as_view(), name='cast-media-list'),
    path('movie_media/create/', views.MovieCreateView.as_view(), name='movie-media-create'),
    path('movie__media_rud/<int:pk>/', views.MovieDetailView.as_view(), name='movie-media-rud'),

    #--------------------------------------------------------------------------------------------
    path('tvshow_media/list/', views.TvShowListView.as_view(), name='tvshow-media-list'),
    path('tvshow_media/create/', views.TVShowCreateView.as_view(), name='tvshow-media-create'),
    path('tvshow__media_rud/<int:pk>/', views.TVShowDetailView.as_view(), name='tvshow-media-rud'), 

    path('season_media/list/', views.SeasonListView.as_view(), name='season-media-list'),   
    path('season_media/create/', views.SeasonCreateView.as_view(), name='season-media-create'),
    path('season__media_rud/<int:pk>/', views.SeasonDetailView.as_view(), name='season-media-rud'),    

    path('epsode_media/list/', views.EpisodeListView.as_view(), name='episode-media-list'),  
    path('episode_media/create/', views.EpisodeCreateView.as_view(), name='episode-media-create'),
    path('episode__media_rud/<int:pk>/', views.EpisodeDetailView.as_view(), name='episode-media-rud'),
    #--------------------------------------------------------------------------------------------
]
