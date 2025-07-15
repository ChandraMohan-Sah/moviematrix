from app6_movie.models import (
    Movie, MovieRatingReview, UserMovieWatchlist,
    UserMovieViewed, MovieVotes, MovieWatchHistory
)
# from app6_movie.api_of_app6_movie.serializers import MovieSerializer
from django.db.models import Q

# def personalized_movie_recommendation(user):
#     # Step 1: Fetch all movie IDs the user has interacted with
#     rated_ids = MovieRatingReview.objects.filter(user_movie_review=user).values_list('movie_id', flat=True)
#     watchlist_ids = UserMovieWatchlist.objects.filter(user_watchlist=user).values_list('movie_id', flat=True)
#     viewed_ids = UserMovieViewed.objects.filter(user_viewed=user).values_list('movie_id', flat=True)
#     voted_ids = MovieVotes.objects.filter(user_vote=user).values_list('movie_id', flat=True)
#     watched_ids = MovieWatchHistory.objects.filter(user=user).values_list('movie_id', flat=True)

#     seen_ids = set(rated_ids) | set(watchlist_ids) | set(viewed_ids) | set(voted_ids) | set(watched_ids)

#     # Step 2: Extract genre, creator, cast preferences from watched movies
#     watched_movies = Movie.objects.filter(id__in=seen_ids)
#     genre_ids = watched_movies.values_list('movie_genre__id', flat=True)
#     creator_ids = watched_movies.values_list('movie_creator__id', flat=True)
#     cast_ids = watched_movies.values_list('movie_cast__id', flat=True)

#     # Step 3: Recommend unseen movies with matching genre, creator, or cast
#     recommended = Movie.objects.exclude(id__in=seen_ids).filter(
#         Q(movie_genre__id__in=genre_ids) |
#         Q(movie_creator__id__in=creator_ids) |
#         Q(movie_cast__id__in=cast_ids)
#     ).distinct().order_by('-movie_created')[:10]  # Use correct timestamp field

#     return recommended


def personalized_movie_recommendation(user):
    # Get all movie IDs user interacted with in one combined query (union)
    rated_ids = MovieRatingReview.objects.filter(user_movie_review=user).values_list('movie_id', flat=True)
    watchlist_ids = UserMovieWatchlist.objects.filter(user_watchlist=user).values_list('movie_id', flat=True)
    viewed_ids = UserMovieViewed.objects.filter(user_viewed=user).values_list('movie_id', flat=True)
    voted_ids = MovieVotes.objects.filter(user_vote=user).values_list('movie_id', flat=True)
    watched_ids = MovieWatchHistory.objects.filter(user=user).values_list('movie_id', flat=True)

    # Combine into a set to remove duplicates
    seen_ids = set(rated_ids) | set(watchlist_ids) | set(viewed_ids) | set(voted_ids) | set(watched_ids)

    if not seen_ids:
        return Movie.objects.order_by('-movie_created').prefetch_related(
            'movie_genre', 'movie_creator', 'movie_cast', 'moviemedia__media_files'
        )[:10]

    watched_movies = Movie.objects.filter(id__in=seen_ids).prefetch_related(
        'movie_genre', 'movie_creator', 'movie_cast'
    )

    genre_ids = watched_movies.values_list('movie_genre__id', flat=True).distinct()
    creator_ids = watched_movies.values_list('movie_creator__id', flat=True).distinct()
    cast_ids = watched_movies.values_list('movie_cast__id', flat=True).distinct()

    # Prefetch media related to movies to avoid N+1 in serializers
    movies_qs = Movie.objects.exclude(id__in=seen_ids).filter(
        Q(movie_genre__id__in=genre_ids) |
        Q(movie_creator__id__in=creator_ids) |
        Q(movie_cast__id__in=cast_ids)
    ).distinct().order_by('-movie_created').prefetch_related(
        'movie_genre', 'movie_creator', 'movie_cast', 'moviemedia__media_files'
    )[:10]

    return movies_qs