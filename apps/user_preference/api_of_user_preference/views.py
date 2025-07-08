from app6_movie.models import (
    MovieRatingReview, UserMovieWatchlist,
    UserMovieViewed, MovieVotes, MovieWatchHistory
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from app6_movie.api_of_app6_movie.serializers import MovieSerializer
from app6_movie.models import Movie

from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='get',
    operation_description="get what users have prefered to see till now",
    operation_id='get what users have prefered to see till now [IsAuthenticated]',
    tags=['User Preferences'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_movie_preferences(request):
    user = request.user
    preferences = {}
    
    # Rated or reviewed
    rated_ids = MovieRatingReview.objects.filter(user_movie_review=user).values_list('movie_id', flat=True)
    rated_movies = Movie.objects.filter(id__in=rated_ids)
    preferences['rated_reviewed'] = MovieSerializer(rated_movies, many=True).data

    # Watchlisted
    watchlisted_ids = UserMovieWatchlist.objects.filter(user_watchlist=user).values_list('movie_id', flat=True)
    watchlisted_movies = Movie.objects.filter(id__in=watchlisted_ids)
    preferences['watchlisted'] = MovieSerializer(watchlisted_movies, many=True).data

    # Viewed
    viewed_ids = UserMovieViewed.objects.filter(user_viewed=user).values_list('movie_id', flat=True)
    viewed_movies = Movie.objects.filter(id__in=viewed_ids)
    preferences['viewed'] = MovieSerializer(viewed_movies, many=True).data

    # Voted
    voted_ids = MovieVotes.objects.filter(user_vote=user).values_list('movie_id', flat=True)
    voted_movies = Movie.objects.filter(id__in=voted_ids)
    preferences['voted'] = MovieSerializer(voted_movies, many=True).data

    # Watched (history)
    watched_ids = MovieWatchHistory.objects.filter(user=user).values_list('movie_id', flat=True)
    watched_movies = Movie.objects.filter(id__in=watched_ids)
    preferences['watched'] = MovieSerializer(watched_movies, many=True).data

    return Response(preferences)

