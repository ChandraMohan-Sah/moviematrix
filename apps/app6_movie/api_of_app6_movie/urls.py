# urls.py
from django.urls import path
from . import views 
 
urlpatterns = [
    path('movies_list/', views.MovieListView.as_view(), name="movie-list-create"),
    path('movies_create/', views.MovieCreateView.as_view(), name="movie-create"),
    path('movies/<int:pk>/', views.Movie_RUD_View.as_view(), name="movie-rud"),
    path('movies_history_list/', views.MovieWatchHistory_L_View.as_view(), name="list-movie-watch-history"),
    path('movies_history_create/', views.MovieWatchHistory_C_View.as_view(), name="create-movie-watch-history"),
    path('movie/<int:pk>/', views.MovieDetail.as_view(), name='movie-detail'),
    
    path('moviesgeneraldetail_list/', views.MovieGeneralDetail_L_View.as_view(), name="moviegeneraldetail-list"),
    path('moviesgeneraldetail_create/', views.MovieGeneralDetail_C_View.as_view(), name="moviegeneraldetail-create"),
    path('moviesgeneraldetail/<int:pk>/', views.MovieGeneralDetail_RUD_View.as_view(), name="moviegeneraldetail-rud"),

    path('moviecoredetail_list/', views.MovieCoreDetail_L_View.as_view(), name="moviecoredetail-list"),
    path('moviecoredetail_create/', views.MovieCoreDetail_C_View.as_view(), name="moviecoredetail-create"),
    path('moviescoredetail/<int:pk>/', views.MovieCoreDetail_RUD_View.as_view(), name="moviecoredetail-rud"),

    path('movieboxofficedetail_list/', views.MovieBoxOffice_L_View.as_view(), name="movieboxofficedetail-list"),
    path('movieboxofficedetail_create/', views.MovieBoxOffice_C_View.as_view(), name="movieboxofficedetail-create"),
    path('movieboxofficedetail/<int:pk>/', views.MovieBoxOffice_RUD_View.as_view(), name="movieboxofficedetail-rud"),

    path('movietechspecsdetail_list/', views.MovieTechSpecs_L_View.as_view(), name="movietechspecsdetail-list"),
    path('movietechspecsdetail_create/', views.MovieTechSpecs_C_View.as_view(), name="movietechspecsdetail-create"),
    path('movietechspecsdetail/<int:pk>/', views.MovieTechSpecs_RUD_View.as_view(), name="movietechspecsdetail-rud"),

    # user specific 
    path('movieratingreview_list/', views.MovieRatingReview_L_View.as_view(), name="movie_rating_review_detail-list"),
    path('movieratingreview_create/', views.MovieRatingReview_C_View.as_view(), name="movie_rating_review_detail-create"),
    path('movieratingreview/<int:pk>/', views.MovieRatingReview_RUD_View.as_view(), name="movie_rating_review_detail-rud"),

    path('usermoviewatchlist/', views.UserMovieWatchlist_List_View.as_view(), name='user-watchlist'),
    path('userwatchlist/toggle/', views.UserMovieWatchlistToggleView.as_view(), name='toggle_watchlist'),

    path('usermovieviewing/', views.UserMovieViewed_List_View.as_view(), name='user-view'),
    path('usermovieviewing/toggle/', views.UserMovieViewedToggleView.as_view(), name='toggle_view'),

    path('usermovievotes/', views.MovieVotes_List_View.as_view(), name='user-movie-votes'),
    path('usermovievotes/toggle/', views.UserMovieVotesToggleView.as_view(), name='toggle-movie-votes'),

]