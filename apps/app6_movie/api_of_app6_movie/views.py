# views.py
from app6_movie.models import  ( 
    Movie, MovieGeneralDetail , MovieCoreDetail, 
    MovieBoxOffice, MovieTechSpecs, MovieRatingReview,
    UserMovieWatchlist, UserMovieViewed, MovieVotes
)

from .serializers import  (
    MovieSerializer, MovieGeneralDetailSerializer, MovieCoreDetailSerializer,
    MovieBoxOfficeSerializer, MovieTechSpecsSerializer, MovieRatingReviewSerializer,
    UserMovieWatchlistSerializer, UserMovieViewedSerializer, MovieVotesSerializer
)

from rest_framework import generics , status
from rest_framework.response import Response

# swagger docs 
from drf_yasg.utils import swagger_auto_schema 
from django.utils.decorators import method_decorator 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='list all  movie',
    operation_description='list all movie',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='create a movie',
    operation_description='create a movie',
)) 
class Movie_LC_View(generics.ListCreateAPIView):
    queryset = Movie.objects.all().select_related('moviemedia').prefetch_related('moviemedia__media_files')
    serializer_class = MovieSerializer 

 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='retrieve particular movie detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='update particular movie detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='patch particular movie detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='delete particular movie detail',
))
class Movie_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all().select_related('moviemedia').prefetch_related('moviemedia__media_files')
    serializer_class = MovieSerializer




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='list all movie general detail',
    operation_description='list all movie general detail',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='create a movie general detail',
    operation_description='create a movie general detail',
))  
class MovieGeneralDetail_LC_View(generics.ListCreateAPIView):
    queryset = MovieGeneralDetail.objects.all().select_related('movie')
    serializer_class = MovieGeneralDetailSerializer 



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='retrieve particular movie general detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='update particular movie general detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='patch particular movie general detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='delete particular movie general detail',
))
class MovieGeneralDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieGeneralDetail.objects.all().select_related('movie')
    serializer_class = MovieGeneralDetailSerializer
 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='list all movie core detail',
    operation_description='list all movie core detail',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='create a movie core detail',
    operation_description='create a movie core detail',
))  
class MovieCoreDetail_LC_View(generics.ListCreateAPIView):
    queryset = MovieCoreDetail.objects.all().select_related('movie')
    serializer_class = MovieCoreDetailSerializer 



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='retrieve particular movie core detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='update particular movie core detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='patch particular movie core detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='delete particular movie core detail',
))
class MovieCoreDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieCoreDetail.objects.all().select_related('movie')
    serializer_class = MovieCoreDetailSerializer
    



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='list all movie  box office  detail',
    operation_description='list all movie tech detail',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='create a movie  box office  detail',
    operation_description='create a movie tech detail',
))  
class MovieBoxOffice_LC_View(generics.ListCreateAPIView):
    queryset = MovieBoxOffice.objects.all().select_related('movie')
    serializer_class = MovieBoxOfficeSerializer 



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='retrieve particular movie box office detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='update particular movie  box office  detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='patch particular movie  box office  detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='delete particular movie  box office  detail',
))
class MovieBoxOffice_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieBoxOffice.objects.all().select_related('movie')
    serializer_class = MovieBoxOfficeSerializer 




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='list all movie tech detail',
    operation_description='list all movie tech detail',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='create a movie tech detail',
    operation_description='create a movie tech detail',
))  
class MovieTechSpecs_LC_View(generics.ListCreateAPIView):
    queryset = MovieTechSpecs.objects.all().select_related('movie')
    serializer_class = MovieTechSpecsSerializer 




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='retrieve particular movie tech detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='update particular movie tech detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='patch particular movie tech detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='delete particular movie tech detail',
))
class MovieTechSpecs_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieTechSpecs.objects.all().select_related('movie')
    serializer_class = MovieTechSpecsSerializer 



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='list all movie review',
    operation_description='list all movie review',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='create a movie review',
    operation_description='create a movie review',
))  
class MovieRatingReview_LC_View(generics.ListCreateAPIView):
    queryset = MovieRatingReview.objects.all().select_related('movie')
    serializer_class = MovieRatingReviewSerializer




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='retrieve particular movie review',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='update particular movie review',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='patch particular movie review',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='delete particular movie review',
))
class MovieRatingReview_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieRatingReview.objects.all().select_related('movie')
    serializer_class = MovieRatingReviewSerializer



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieUserVotes APIs'], operation_id='list all movie votes',
    operation_description='list all movie votes',
))
class MovieVotes_List_View(generics.ListAPIView):
    queryset = MovieVotes.objects.all().select_related('movie')
    serializer_class = MovieVotesSerializer



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieUserVotes APIs'], operation_id='give vote on movie',
    operation_description='give vote on movie',
)) 
class UserMovieVotesToggleView(generics.CreateAPIView):
    serializer_class = MovieVotesSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        movie = request.data.get('movie_id')

        # Check for existing entry
        existing = MovieVotes.objects.filter(user_vote_id=user, movie_id=movie).first()

        if existing:
            existing.delete()
            return Response({'detail': 'user removed the vote.'}, status=status.HTTP_200_OK)
        else:
            # Create new watchlist entry
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)





@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieUserWatchlist APIs'], operation_id='list all user watchlist',
    operation_description='list all user watchlist',
))
class UserMovieWatchlist_List_View(generics.ListAPIView):
    queryset = UserMovieWatchlist.objects.all().select_related('movie')
    serializer_class = UserMovieWatchlistSerializer



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieUserWatchlist APIs'], operation_id='create a user watchlist',
    operation_description='create a user watchlist',
)) 
class UserMovieWatchlistToggleView(generics.CreateAPIView):
    serializer_class = UserMovieWatchlistSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        movie = request.data.get('movie_id')

        # Check for existing entry
        existing = UserMovieWatchlist.objects.filter(user_watchlist_id=user, movie_id=movie).first()

        if existing:
            existing.delete()
            return Response({'detail': 'Removed from watchlist'}, status=status.HTTP_200_OK)
        else:
            # Create new watchlist entry
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieUserViewed APIs'], operation_id='list all user viewing list',
    operation_description='list all user viewing list',
))
class UserMovieViewed_List_View(generics.ListAPIView):
    queryset = UserMovieViewed.objects.all().select_related('movie')
    serializer_class = UserMovieViewedSerializer



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieUserViewed APIs'], operation_id='create a user viewing history',
    operation_description='create a user viewing history',
)) 
class UserMovieViewedToggleView(generics.CreateAPIView):
    serializer_class = UserMovieViewedSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        movie = request.data.get('movie_id')

        # Check for existing entry
        existing = UserMovieViewed.objects.filter(user_viewed_id=user, movie_id=movie).first()

        if existing:
            existing.delete()
            return Response({'detail': 'Removed from viewing history'}, status=status.HTTP_200_OK)
        else:
            # Create new watchlist entry
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



