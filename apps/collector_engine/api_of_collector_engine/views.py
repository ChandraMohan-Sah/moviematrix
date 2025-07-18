from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from django.core.cache import cache
from django.db.models import Avg
from django.db.models import Count

from app6_movie.models import Movie, MovieWatchHistory
from app6_movie.api_of_app6_movie.serializers import MovieReadSerializer 
from .serializers import (
    LightMovieSerializer, PopularCastSerializer, IMDBOriginalsSerializer
)

from app3_cast.models import Cast
from app3_cast.api_of_app3_cast.serializers import CastSerializer

import random
from datetime import timedelta
from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema

# Background task using celery  + paginate 10 

'''Popular Celebrity|Cast'''
# collect - fetch cast of (movie, tvshow) with maximum rating
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 popular cast based on average movie rating.",
    operation_id='get popular cast',
    responses={200: CastSerializer(many=True)},
    tags=['Collector Engine'],
)
@api_view(['GET'])
def get_popular_cast(request):
    cache_key = 'popular_cast'
    casts = cache.get(cache_key)

    if casts is None:
        # Annotate each cast with the avg rating of movies they are in 
        casts = list(
            Cast.objects.annotate(
                avg_rating = Avg('movie_cast__movie_general_detail__avg_rating') # Cast → Movie → MovieGeneralDetail → avg_rating
            )
            .select_related('castmedia')
            .prefetch_related('castmedia__media_files')  # Prefetch media files for each cast
            .order_by('-avg_rating')[:10]
        )
        cache.set(cache_key, casts, timeout=100) # 1hr
    
    serialized = PopularCastSerializer(casts, many=True)
    return Response(serialized.data)



'''Fan Favourites'''
# collect - movies with top ratings
# collect - movies with most number of  votes
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 fan favourites movie based on average movie rating and votes.",
    operation_id='get fan favourites',
    responses={200: LightMovieSerializer(many=True)},
    tags=['Collector Engine'],
)
@api_view(['GET'])
def get_fan_favourites(request):
    cache_key = 'fan_favourites'
    movies = cache.get(cache_key)

    if movies is None:
        movies = list(
            Movie.objects.annotate(
                avg_rating=Avg('movie_reviews__rating'),
                num_votes=Count('votes')
            )
            .select_related('moviemedia')
            .prefetch_related('moviemedia__media_files')  # Prefetch media files for each movie
            .order_by('-avg_rating', '-num_votes')[:10]
        )
        cache.set(cache_key, movies, timeout=100)
    
    serialized = LightMovieSerializer(movies, many=True)
    return Response(serialized.data)



'''Popular Movies'''
# collect - movie with maximum reviews 
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 popular movies based on average movie votes.",
    operation_id='get popular movie',
    responses={200: LightMovieSerializer(many=True)},
    tags=['Collector Engine'],
) 
@api_view(['GET'])
def get_popular_movies(request):
    cache_key = 'popular_movies'
    movies = cache.get(cache_key)

    if movies is None:
        movies = list(
            Movie.objects
            .select_related('moviemedia', 'movie_general_detail')
            .prefetch_related('moviemedia__media_files')
            .order_by('-movie_general_detail__avg_rating')[:10]
        )
        cache.set(cache_key, movies, timeout=3600)  # cache for 1 hour

    serialized = LightMovieSerializer(movies, many=True)
    return Response(serialized.data)
 




'''IMDB Originals'''
# collect - is_original=True (random function )
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 imdb original movies.",
    operation_id='get imdb original movie',
    responses={200: IMDBOriginalsSerializer(many=True)},
    tags=['Collector Engine'],
) 
@api_view(['GET'])
def get_imdb_originals(request):
    cache_key = 'imdb_originals'
    movies_data = cache.get(cache_key)

    if movies_data is None:
        # Filter original movies only
        originals_qs = Movie.objects.filter(movie_general_detail__is_original=True) \
            .select_related('moviemedia') \
            .prefetch_related('moviemedia__media_files')

        # Random sampling inside DB if small dataset or load-efficient way
        all_ids = list(originals_qs.values_list('id', flat=True))
        sample_ids = random.sample(all_ids, min(10, len(all_ids)))

        sampled_qs = originals_qs.filter(id__in=sample_ids)

        serializer = IMDBOriginalsSerializer(sampled_qs, many=True)
        movies_data = serializer.data

        cache.set(cache_key, movies_data, timeout=600)  # cache for 1 hr
    return Response(movies_data)

 


'''Prime Video'''
# collect platform = prime (random function)
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 prime video movies.",
    operation_id='get top 10 prime video movies.',
    responses={200: LightMovieSerializer(many=True)},
    tags=['Collector Engine'],
) 
@api_view(['GET'])
def get_prime_video(request):
    cache_key = 'prime_videos'
    movies_data = cache.get(cache_key)

    if movies_data is None:
        prime_videos_qs = Movie.objects.filter(
            platform__platform__iexact='prime'
        ).select_related('moviemedia') \
         .prefetch_related('moviemedia__media_files')[:10]

        serializer = LightMovieSerializer(prime_videos_qs, many=True)
        movies_data = serializer.data

        cache.set(cache_key, movies_data, timeout=60 * 60)  # Cache for 1 hour
    return Response(movies_data)



'''In Theaters'''
# collect by release date <= today <= release_date + 8 weeks (random function)
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 movies currently in theaters.",
    operation_id='get top 10 movies in theaters.',
    responses={200: MovieReadSerializer(many=True)},
    tags=['Collector Engine'],
) 
@api_view(['GET'])
def get_in_theaters(request):
    cache_key = 'in_theaters'
    movies = cache.get(cache_key)

    if movies is None:
        today = timezone.now().date()

        in_theaters = Movie.objects.filter(
            movie_core_detail__release_date__lte=today,
            movie_core_detail__release_date__gte=today - timedelta(weeks=8)
        ).select_related('moviemedia') \
        .prefetch_related('moviemedia__media_files')[:10]
        

        serializer = LightMovieSerializer(in_theaters, many=True)
        movies = serializer.data
        cache.set(cache_key, movies, timeout=100)  # cache for 1 hour

    return Response(list(movies))



'''Coming Soon to Theaters + Editors Picks'''
# collect : release_date > today (random function)
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 comming soon movies  in theaters.",
    operation_id='get top 10 movies that is comming soon.',
    responses={200: MovieReadSerializer(many=True)},
    tags=['Collector Engine'],
) 
@api_view(['GET'])
def get_coming_soon_editors_pick(request):
    cache_key = 'coming_soon_editors_pick'
    movies_data = cache.get(cache_key)

    if movies_data is None:
        today = timezone.now().date()

        # Filter upcoming releases
        upcoming_qs = Movie.objects.filter(
            movie_core_detail__release_date__gt=today
        ).select_related('moviemedia') \
         .prefetch_related('moviemedia__media_files')

        # Efficient sampling without loading full objects
        all_ids = list(upcoming_qs.values_list('id', flat=True))
        sampled_ids = random.sample(all_ids, min(10, len(all_ids)))

        sampled_movies = upcoming_qs.filter(id__in=sampled_ids)

        serializer = MovieReadSerializer(sampled_movies, many=True)
        movies_data = serializer.data
        cache.set(cache_key, movies_data, timeout=100)  # cache for 100 seconds

    return Response(movies_data)



'''Your May Like '''
# collect user specific


'''Recently Viewed : Watch History '''
# collect user specific 
@swagger_auto_schema(
    method='get',
    operation_description="User Watch History",
    operation_id='User Watch History',
    responses={200: MovieReadSerializer(many=True)},
    tags=['Collector Engine'],
) 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recently_viewed_movies(request):
    user = request.user

    # Fetch latest 10 watched movie IDs by this user (distinct movie_id order)
    recent_movie_ids = (
        MovieWatchHistory.objects.filter(user=user)
        .order_by('-watched_at')
        .values_list('movie_id', flat=True)
        .distinct()[:10]
    )

    # Fetch Movie objects (add related fields to avoid N+1)
    movies = Movie.objects.filter(id__in=recent_movie_ids) \
        .select_related('moviemedia') \
        .prefetch_related('moviemedia__media_files')

    # Sort the movies in the same order as recent_movie_ids
    movie_dict = {movie.id: movie for movie in movies}
    ordered_movies = [movie_dict[mid] for mid in recent_movie_ids if mid in movie_dict]

    serializer = MovieReadSerializer(ordered_movies, many=True)
    return Response(serializer.data)





  
# ---------Page Wise Collection ------------------------

''' For Movie Page '''
def collect_featured_movies():
    # one recent movie with maximum rating
    # one recent movie with maximum likes
    pass


''' For Tvshow Page '''
def collect_featured_tvshow():
    # one recent tvshow with maximum rating 
    # one recent tvshow with maximum likes
    pass


''' For Episode Page '''
def collect_featured_episode():
    # one recent episode with maximum rating 
    # one recent episode with maximum likes 
    pass


''' For Home Page'''
def collect_featured_home():
    # one recent movie with maximum rating
    # one recent movie with maximum likes
    # one recent tvshow with maximum rating 
    # one recent tvshow with maximum likes
    # one recent episode with maximum rating 
    # one recent episode with maximum likes 
    pass

# -----------------------------------------------------
