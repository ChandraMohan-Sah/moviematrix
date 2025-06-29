# serializers.py
from rest_framework import serializers
from user_dashboard.models import UserDashboard

from app7_tvshow.models import UserTvShowWatchlist
from app7_tvshow.api_of_app7_tvshow.serializers import (
    UserTvShowWatchlistSerializer, UserTvShowViewedSerializer,
    TvShowRatingReviewSerializer
)

from app6_movie.api_of_app6_movie.serializers import (
    UserMovieWatchlistSerializer, UserMovieViewedSerializer,
    MovieRatingReviewSerializer

) 

from app10_episode.api_of_app10_episode.serializers import (
    UserEpisodeWatchlistSerializer, UserEpisodeViewedSerializer,
    EpisodeRatingReviewSerializer

)

from user_profile.api_of_user_profile.serializers import (
    CompleteUserProfileInfoSerializer
)

from rest_framework.response import Response

'''
    obj : is a User instance.
    obj.episode_watchlist : is the RelatedManager for all EpisodeWatchlist rows linked to that user.
    So qs is a queryset : of EpisodeWatchlist instances related to this user.
'''


class UserDashboardSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    # properties that return querysets
    movie_watchlist = serializers.SerializerMethodField()
    tvshow_watchlist = serializers.SerializerMethodField()
    episode_watchlist = serializers.SerializerMethodField()
    
    movie_viewed = serializers.SerializerMethodField()
    tvshow_viewed = serializers.SerializerMethodField()
    episode_viewed = serializers.SerializerMethodField()

    movie_ratings_reviews = serializers.SerializerMethodField()
    tvshow_rating_reviews = serializers.SerializerMethodField()
    episode_rating_reviews = serializers.SerializerMethodField()

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
        ]


    def get_profile(self, obj):
        request = self.context.get('request')
        user = request.user

        if hasattr(user, 'profile'):
            return CompleteUserProfileInfoSerializer(user.profile).data
        return None


    def get_movie_watchlist(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return Response(" Please authenticate first !")
        
        user = request.user
        qs = obj.movie_watchlist.filter(user_watchlist=user)
        return UserMovieWatchlistSerializer(qs, many=True).data
            

    def get_tvshow_watchlist(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return Response(" Please authenticate first !")

        user = request.user
        qs = obj.tvshow_watchlist.filter(user_watchlist=user)
        return UserTvShowWatchlistSerializer(qs, many=True).data


    def get_episode_watchlist(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return Response(" Please authenticate first !")
        
        user = request.user
        qs = obj.episode_watchlist.filter(user_watchlist=user)
        return UserEpisodeWatchlistSerializer(qs, many=True).data
        

    def get_movie_viewed(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return Response(" Please authenticate first !")
        
        user = request.user
        qs = obj.movie_viewed.filter(user_viewed=user)
        return UserMovieViewedSerializer(qs, many=True).data


    def get_tvshow_viewed(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return Response(" Please authenticate first !")
        
        user = request.user
        qs = obj.movie_viewed.filter(user_viewed=user)
        return UserTvShowViewedSerializer(qs, many=True).data
        

    def get_episode_viewed(self, obj):  
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return Response(" Please authenticate first !")
        
        user = request.user
        qs = obj.episode_viewed.filter(user_viewed=user)
        return UserEpisodeViewedSerializer(qs, many=True).data 
    

    def get_movie_ratings_reviews(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return Response(" Please authenticate first !")
        
        user = request.user
        qs = obj.movie_ratings_reviews.filter(user_movie_review=user)
        return MovieRatingReviewSerializer(qs, many=True).data


    def get_tvshow_rating_reviews(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return Response(" Please authenticate first !")
        
        user = request.user
        qs = obj.tvshow_rating_reviews.filter(user_tvshow_review=user)
        return TvShowRatingReviewSerializer(qs, many=True).data


    def get_episode_rating_reviews(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return Response(" Please authenticate first !")
        
        user = request.user
        qs = obj.episode_rating_reviews.filter(user_episode_review=user)
        return EpisodeRatingReviewSerializer(qs, many=True).data 
    
