# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('episodes/', views.Episode_LC_View.as_view(), name="episode-list-create"),
    path('episodes/<int:pk>/', views.Episode_RUD_View.as_view(), name="episode-rud"),
    path('episode_history/', views.EpisodeWatchHistoryView.as_view(), name="episode-watch-history"),

    path('episodes_general_detail/', views.EpisodeGeneralDetail_LC_View.as_view(), name="episode-general-detail-list-create"),
    path('episodes_general_detail/<int:pk>/', views.EpisodeGeneralDetail_RUD_View.as_view(), name="episode-general-detail-rud"),

    path('episodes_watchlist/', views.EpisodeUserWatchlist_LC_View.as_view(), name="episode-watchlist-list"),
    path('episodes_watchlist/toggle/', views.UserEpisodeWatchlistToggleView.as_view(), name="episode-watchlist-toggle"),

    path('episodes_viewed/', views.EpisodeUserViewed_LC_View.as_view(), name="episode-viewed-list"),
    path('episodes_viewed/toggle/', views.UserEpisodeViewedToggleView.as_view(), name="episode-add-viewing-toggle"),

    path('episodes_votes/', views.EpisodeVotes_List_View.as_view(), name="user-added-vote-on-episode-list"),
    path('episodes_votes/toggle/', views.EpisodeVotesToggleView.as_view(), name="user-added-vote-on-episode-toggle"),

    path('episodes_rating_review/', views.EpisodeRatingReview_LC_View.as_view(), name="episode-rating-review-list"),
    path('episodes_rating_review/<int:pk>/', views.EpisodeRatingReview_RUD_View.as_view(), name="episode-rating-review-detail"),
]
