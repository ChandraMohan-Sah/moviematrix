# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('tvshows/', views.TvShow_LC_View.as_view(), name="tvshow-list-create"),
    path('tvshows/<int:pk>/', views.TvShow_RUD_View.as_view(), name="tvshow-rud"),
    
    path('tvshows_general_detail/', views.TvShowGeneralDetail_LC_View.as_view(), name="tvshow-general-detail-list-create"),
    path('tvshows_general_detail/<int:pk>/', views.TvShowGeneralDetail_RUD_View.as_view(), name="tvshow-general-detail-rud"),

    path('tvshows_core_detail/', views.TvShowCoreDetail_LC_View.as_view(), name="tvshow-core-detail-list-create"),
    path('tvshows_core_detail/<int:pk>/', views.TvShowCoreDetail_RUD_View.as_view(), name="tvshow-core-detail-rud"),

    path('tvshows_tech_specs_detail/', views.TvShowTechSpecsDetail_LC_View.as_view(), name="tvshow-tech-specs-detail-list-create"),
    path('tvshows_tech_specs_detail/<int:pk>/', views.TvShowTechSpecsDetail_RUD_View.as_view(), name="tvshow-tech-specs-detail-rud"),

    path('tvshows_rating_review_detail/', views.TvShowRatingReview_LC_View.as_view(), name="tvshow-rating-review-list-create"),
    path('tvshows_rating_review_detail/<int:pk>/', views.TvShowRatingReview_RUD_View.as_view(), name="tvshow-rating-review-rud"),

    path('tvshows_votes/', views.TvShowVotes_List_View.as_view(), name="tvshow-votes-list-create"),
    path('tvshows_votes/toggle/', views.UserTvShowVotesToggleView.as_view(), name="tvshow-votes-rud"),
    
    path('tvshows_watchlist/', views.UserTvShowWatchlist_List_View.as_view(), name="tvshow-watchlist-list-create"),
    path('tvshows_watchlist/toggle/', views.UserTvShowWatchlistToggleView.as_view(), name="tvshow-watchlist-rud"),

    path('tvshows_viewed/', views.UserTvShowViewed_List_View.as_view(), name="tvshow-watchlist-list-create"),
    path('tvshows_viewed/toggle/', views.UserTvShowViewedToggleView.as_view(), name="tvshow-watchlist-rud"),
    
]
