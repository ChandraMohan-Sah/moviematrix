from rest_framework import serializers
from user_dashboard.models import UserDashboard
from app7_tvshow.models import UserTvShowWatchlist
from app7_tvshow.api_of_app7_tvshow.serializers import (
    UserTvShowWatchlistSerializer, UserTvShowViewedSerializer,
    TvShowRatingReviewSerializer
)
from app6_movie.api_of_app6_movie.serializers import (
    UserMovieWatchlistSerializer, UserMovieViewedSerializer,
    MovieRatingReviewSerializer, MovieWatchHistorySerializer
)
from app10_episode.api_of_app10_episode.serializers import (
    UserEpisodeWatchlistSerializer, UserEpisodeViewedSerializer,
    EpisodeRatingReviewSerializer
)
from user_profile.api_of_user_profile.serializers import (
    CompleteUserProfileInfoSerializer
)

class UserDashboardSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    movie_watchlist = serializers.SerializerMethodField()
    tvshow_watchlist = serializers.SerializerMethodField()
    episode_watchlist = serializers.SerializerMethodField()
    movie_viewed = serializers.SerializerMethodField()
    tvshow_viewed = serializers.SerializerMethodField()
    episode_viewed = serializers.SerializerMethodField()
    movie_ratings_reviews = serializers.SerializerMethodField()
    tvshow_rating_reviews = serializers.SerializerMethodField()
    episode_rating_reviews = serializers.SerializerMethodField()
    movie_watch_history = serializers.SerializerMethodField()

    class Meta:
        model = UserDashboard
        fields = [
            'profile',
            'movie_watchlist',
            'tvshow_watchlist',
            'episode_watchlist',
            'movie_viewed',
            'tvshow_viewed',
            'episode_viewed',
            'movie_ratings_reviews',
            'tvshow_rating_reviews',
            'episode_rating_reviews',
            'movie_watch_history'
        ]


    def get_profile(self, obj):
        if hasattr(obj.user, 'profile'):
            return CompleteUserProfileInfoSerializer(obj.user.profile, context=self.context).data
        return None

    def get_movie_watchlist(self, obj):
        print("CONTEXT CONTENT:", self.context) 
        qs = obj.movie_watchlist
        return UserMovieWatchlistSerializer(qs, many=True, context=self.context).data

    def get_tvshow_watchlist(self, obj):
        qs = obj.tvshow_watchlist
        return UserTvShowWatchlistSerializer(qs, many=True, context=self.context).data

    def get_episode_watchlist(self, obj):
        qs = obj.episode_watchlist
        return UserEpisodeWatchlistSerializer(qs, many=True, context=self.context).data

    def get_movie_viewed(self, obj):
        qs = obj.movie_viewed
        return UserMovieViewedSerializer(qs, many=True, context=self.context).data

    def get_tvshow_viewed(self, obj):
        qs = obj.tvshow_viewed  # Fixed: Changed movie_viewed to tvshow_viewed
        return UserTvShowViewedSerializer(qs, many=True, context=self.context).data

    def get_episode_viewed(self, obj):
        qs = obj.episode_viewed
        return UserEpisodeViewedSerializer(qs, many=True, context=self.context).data

    def get_movie_ratings_reviews(self, obj):
        qs = obj.movie_ratings_reviews
        return MovieRatingReviewSerializer(qs, many=True, context=self.context).data

    def get_tvshow_rating_reviews(self, obj):
        qs = obj.tvshow_rating_reviews
        return TvShowRatingReviewSerializer(qs, many=True, context=self.context).data

    def get_episode_rating_reviews(self, obj):
        qs = obj.episode_rating_reviews
        print(f"User: {obj.user.username}, Rating Review QS: {qs}")
        return EpisodeRatingReviewSerializer(qs, many=True, context=self.context).data

    def get_movie_watch_history(self, obj):
        qs = obj.movie_watch_history
        print(f"User: {obj.user.username}, Watch History QS: {qs}")
        return MovieWatchHistorySerializer(qs, many=True, context=self.context).data