# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('title/', views.TitleList.as_view(), name='title-list'),
    path('cast/', views.CastList.as_view(), name='cast-list'),
    path('creator/', views.CreatorList.as_view(), name='creator-list'),
    path('writer/', views.WriterList.as_view(), name='writer-list'),

    # # filtering [predefined tags]
    path('based-on/movie/cast/', views.BasedOn_Movie_Cast.as_view(), name='based-on-movie-cast'),
    # path('based-on/tvshow/cast/', views.BasedOn_TvShow_Cast.as_view(), name='based-on-tvshow-cast'),

    path('based-on/movie/ratings/', views.BasedOn_Movie_Ratings.as_view(), name='based-on-movie-ratings'),
    # path('based-on/tvshow/ratings/', views.BasedOn_TvShow_Ratings.as_view(), name='based-on-tvshow-ratings'),
    # path('based-on/episode/ratings/', views.BasedOn_Episode_Ratings.as_view(), name='based-on-episode-ratings'),

    path('based-on/movie/genre/', views.BasedOn_Movie_Genre.as_view(), name='based-on-movie-genre'),
    # path('based-on/movie/ontheater/', views.BasedOn_Movie_InTheaters.as_view(), name='based-on-movie-theater')
]




