# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.Movie_LC_View.as_view(), name="movie-list-create"),
    path('movies/<int:pk>/', views.Movie_RUD_View.as_view(), name="movie-rud"),
    path('movies_history/', views.MovieWatchHistoryView.as_view(), name="movie-watch-history"),
    
    path('moviesgeneraldetail/', views.MovieGeneralDetail_LC_View.as_view(), name="moviegeneraldetail-list-create"),
    path('moviesgeneraldetail/<int:pk>/', views.MovieGeneralDetail_RUD_View.as_view(), name="moviegeneraldetail-rud"),

    path('moviecoredetail/', views.MovieCoreDetail_LC_View.as_view(), name="moviecoredetail-list-create"),
    path('moviescoredetail/<int:pk>/', views.MovieCoreDetail_RUD_View.as_view(), name="moviecoredetail-rud"),

    path('movieboxofficedetail/', views.MovieBoxOffice_LC_View.as_view(), name="movieboxofficedetail-list-create"),
    path('movieboxofficedetail/<int:pk>/', views.MovieBoxOffice_RUD_View.as_view(), name="movieboxofficedetail-rud"),

    path('movietechspecsdetail/', views.MovieTechSpecs_LC_View.as_view(), name="movietechspecsdetail-list-create"),
    path('movietechspecsdetail/<int:pk>/', views.MovieTechSpecs_RUD_View.as_view(), name="movietechspecsdetail-rud"),

    # user specific 
    path('movieratingreview/', views.MovieRatingReview_LC_View.as_view(), name="movie_rating_review_detail-list-create"),
    path('movieratingreview/<int:pk>/', views.MovieRatingReview_RUD_View.as_view(), name="movie_rating_review_detail-rud"),

    path('usermoviewatchlist/', views.UserMovieWatchlist_List_View.as_view(), name='user-watchlist'),
    path('userwatchlist/toggle/', views.UserMovieWatchlistToggleView.as_view(), name='toggle_watchlist'),

    path('usermovieviewing/', views.UserMovieViewed_List_View.as_view(), name='user-view'),
    path('usermovieviewing/toggle/', views.UserMovieViewedToggleView.as_view(), name='toggle_view'),

    path('usermovievotes/', views.MovieVotes_List_View.as_view(), name='user-movie-votes'),
    path('usermovievotes/toggle/', views.UserMovieVotesToggleView.as_view(), name='toggle-movie-votes'),

]