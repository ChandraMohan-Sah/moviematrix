from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from django.core.cache import cache
from django.db.models import Avg
from django.db.models import Count

from app6_movie.models import Movie, MovieWatchHistory
from app6_movie.api_of_app6_movie.serializers import MovieSerializer
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
            ).order_by('-avg_rating')[:10]
        )
        cache.set(cache_key, casts, timeout=100) # 1hr
    
    serialized = CastSerializer(casts, many=True)
    return Response(serialized.data)



'''Fan Favourites'''
# collect - movies with top ratings
# collect - movies with most number of  votes
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 fan favourites movie based on average movie rating and votes.",
    operation_id='get fan favourites',
    responses={200: MovieSerializer(many=True)},
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
            ).order_by('-avg_rating', '-num_votes')[:10]
        )
        cache.set(cache_key, movies, timeout=100)
    
    serialized = MovieSerializer(movies, many=True)
    return Response(serialized.data)
    


'''Popular Movies'''
# collect - movie with maximum reviews 
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 popular movies based on average movie votes.",
    operation_id='get popular movie',
    responses={200: MovieSerializer(many=True)},
    tags=['Collector Engine'],
) 
@api_view(['GET'])
def get_popular_movies(request):
    cache_key = 'popular_movies'
    movies = cache.get(cache_key)

    if movies is None:
        movies = list(
            Movie.objects.annotate(
                num_votes=Count('votes')
            ).order_by('-num_votes')[:10]
        )
        cache.set(cache_key, movies, timeout=100) # 1hr

    serialized = MovieSerializer(movies, many=True)
    return Response(serialized.data)




'''IMDB Originals'''
# collect - is_original=True (random function )
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 imdb original movies.",
    operation_id='get imdb original movie',
    responses={200: MovieSerializer(many=True)},
    tags=['Collector Engine'],
) 
@api_view(['GET'])
def get_imdb_originals(request):
    cache_key = 'imdb_originals'
    movies = cache.get(cache_key)

    if movies is None:
        originals = Movie.objects.filter(movie_general_detail__is_original=True)
        sampled_movies = random.sample(
            list(originals),
            min(10, originals.count())
        )
        serializer = MovieSerializer(sampled_movies, many=True)
        movies = serializer.data 

        cache.set(cache_key, movies, timeout=100)

    return Response(list(movies))


 


'''Prime Video'''
# collect platform = prime (random function)
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 prime video movies.",
    operation_id='get top 10 prime video movies.',
    responses={200: MovieSerializer(many=True)},
    tags=['Collector Engine'],
) 
@api_view(['GET'])
def get_prime_video(request):
    cache_key = 'prime_videos'
    movies = cache.get(cache_key)

    if movies is None: 
        prime_videos = Movie.objects.filter(
            platform__platform__iexact='prime'
        )[:10]

        serializer = MovieSerializer(prime_videos, many=True)
        movies = serializer.data 

        cache.set(cache_key, movies, timeout=100)

    return Response(list(movies))



'''In Theaters'''
# collect by release date <= today <= release_date + 8 weeks (random function)
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 movies currently in theaters.",
    operation_id='get top 10 movies in theaters.',
    responses={200: MovieSerializer(many=True)},
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
        )

        serializer = MovieSerializer(in_theaters, many=True)
        movies = serializer.data
        cache.set(cache_key, movies, timeout=100)  # cache for 1 hour

    return Response(list(movies))



'''Coming Soon to Theaters + Editors Picks'''
# collect : release_date > today (random function)
@swagger_auto_schema(
    method='get',
    operation_description="Get top 10 comming soon movies  in theaters.",
    operation_id='get top 10 movies that is comming soon.',
    responses={200: MovieSerializer(many=True)},
    tags=['Collector Engine'],
) 
@api_view(['GET'])
def get_coming_soon_editors_pick(request):
    cache_key = 'coming_soon_editors_pick'
    movies = cache.get(cache_key)

    if movies is None:
        today = timezone.now().date()

        coming_soon = Movie.objects.filter(
            movie_core_detail__release_date__gt=today
        )

        # Randomly select up to 10 movies as Editor's Picks
        sampled = random.sample(list(coming_soon), min(10, coming_soon.count()))

        serializer = MovieSerializer(sampled, many=True)
        movies = serializer.data

        cache.set(cache_key, movies, timeout=100)  # cache for 100 sec

    return Response(list(movies))



'''Your May Like '''
# collect user specific


'''Recently Viewed : Watch History '''
# collect user specific 
@swagger_auto_schema(
    method='get',
    operation_description="User Watch History",
    operation_id='User Watch History',
    responses={200: MovieSerializer(many=True)},
    tags=['Collector Engine'],
) 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recently_viewed_movies(request):
    user = request.user

    # Fetch latest 10 watched movie IDs by this user (avoid duplicate movies)
    recent_movie_ids = (
        MovieWatchHistory.objects.filter(user=user)
        .order_by('-watched_at')
        .values_list('movie_id', flat=True)
        .distinct()[:10]
    )

    # Fetch Movie objects in the same order as IDs
    movies = Movie.objects.filter(id__in=recent_movie_ids)
    # Optional: maintain order as per watched_at
    movies = sorted(movies, key=lambda x: recent_movie_ids.index(x.id))

    serializer = MovieSerializer(movies, many=True)
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
