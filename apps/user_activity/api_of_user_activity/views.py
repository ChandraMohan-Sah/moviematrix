from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models import Count
from app6_movie.models import MovieWatchHistory, Movie
from app6_movie.api_of_app6_movie.serializers import MovieReadSerializer

from app7_tvshow.models import TvShowWatchHistory, TvShow
from app7_tvshow.api_of_app7_tvshow.serializers  import TvShowSerializer

from app10_episode.models import EpisodeWatchHistory, Episode
from app10_episode.api_of_app10_episode.serializers import EpisodeSerializer

# swagger ui integration
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='get',
    operation_description="get recently viewed movies.",
    operation_id='get recently viewed movies [IsAuthenticated]',
    tags=['User Activity'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_activity(request):
    user = request.user
    cache_key = f'user_activity_{user.id}'
    data = cache.get(cache_key)

    if not data:
        movie_ids = list(
            MovieWatchHistory.objects.filter(user=user)
            .order_by('-watched_at')
            .values_list('movie_id', flat=True)
            .distinct()[:10]
        )
        movies = Movie.objects.filter(id__in=movie_ids)
        movies = sorted(movies, key=lambda x: movie_ids.index(x.id))

        tvshow_ids = list(
            TvShowWatchHistory.objects.filter(user=user)
            .order_by('-watched_at')
            .values_list('tvshow_id', flat=True)
            .distinct()[:10]
        )
        tvshows = TvShow.objects.filter(id__in=tvshow_ids)
        tvshows = sorted(tvshows, key=lambda x: tvshow_ids.index(x.id))

        episode_ids = list(
            EpisodeWatchHistory.objects.filter(user=user)
            .order_by('-watched_at')
            .values_list('episode_id', flat=True)
            .distinct()[:10]
        )
        episodes = Episode.objects.filter(id__in=episode_ids)
        episodes = sorted(episodes, key=lambda x: episode_ids.index(x.id))

        data = {
            'recent_movies': MovieReadSerializer(movies, many=True).data,
            'recent_tvshows': TvShowSerializer(tvshows, many=True).data,
            'recent_episodes': EpisodeSerializer(episodes, many=True).data,
        }

        cache.set(cache_key, data, timeout=300)

    return Response(data)

