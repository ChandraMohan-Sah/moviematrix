from app6_movie.models import (
    MovieRatingReview, UserMovieWatchlist,
    UserMovieViewed, MovieVotes, MovieWatchHistory
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from app6_movie.api_of_app6_movie.serializers import MovieReadSerializer
from app6_movie.models import Movie
from django.core.cache import cache

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
    cache_key = f'user_prefs_{user.id}'

    data = cache.get(cache_key)
    if data:
        return Response(data)

    rated_ids = set(MovieRatingReview.objects.filter(user_movie_review=user).values_list('movie_id', flat=True))
    watchlisted_ids = set(UserMovieWatchlist.objects.filter(user_watchlist=user).values_list('movie_id', flat=True))
    viewed_ids = set(UserMovieViewed.objects.filter(user_viewed=user).values_list('movie_id', flat=True))
    voted_ids = set(MovieVotes.objects.filter(user_vote=user).values_list('movie_id', flat=True))
    watched_ids = set(MovieWatchHistory.objects.filter(user=user).values_list('movie_id', flat=True))

    all_ids = rated_ids | watchlisted_ids | viewed_ids | voted_ids | watched_ids

    movie_qs = Movie.objects.filter(id__in=all_ids) \
        .select_related('moviemedia') \
        .prefetch_related('moviemedia__media_files')

    movie_map = {movie.id: movie for movie in movie_qs}

    data = {
        'rated_reviewed': MovieReadSerializer([movie_map[mid] for mid in rated_ids if mid in movie_map], many=True).data,
        'watchlisted': MovieReadSerializer([movie_map[mid] for mid in watchlisted_ids if mid in movie_map], many=True).data,
        'viewed': MovieReadSerializer([movie_map[mid] for mid in viewed_ids if mid in movie_map], many=True).data,
        'voted': MovieReadSerializer([movie_map[mid] for mid in voted_ids if mid in movie_map], many=True).data,
        'watched': MovieReadSerializer([movie_map[mid] for mid in watched_ids if mid in movie_map], many=True).data,
    }

    cache.set(cache_key, data, timeout=300)
    return Response(data)


