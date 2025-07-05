# views.py
from app6_movie.models import  ( 
    Movie, MovieGeneralDetail , MovieCoreDetail, 
    MovieBoxOffice, MovieTechSpecs, MovieRatingReview,
    UserMovieWatchlist, UserMovieViewed, MovieVotes, MovieWatchHistory
)

from .serializers import  (
    MovieSerializer, MovieGeneralDetailSerializer, MovieCoreDetailSerializer,
    MovieBoxOfficeSerializer, MovieTechSpecsSerializer, MovieRatingReviewSerializer,
    UserMovieWatchlistSerializer, UserMovieViewedSerializer, MovieVotesSerializer,
    MovieWatchHistorySerializer
)

from rest_framework import generics , status
from rest_framework.response import Response

#pagination 
from rest_framework import pagination
from rest_framework.decorators import permission_classes
from shared.pagination import GlobalPagination


#permissions
from rest_framework import permissions
from shared.permissions import IsAdminOrReadOnly
from .custom_permission import  ( 
    IsMovieReviewer_OrReadOnly, IsMovieVoter_OrReadOnly, 
    IsUserMovieWatchlist_OrReadOnly,IsAdminOrUserWatchlistedMovie,
    IsUserViewedMovie_OrReadOnly, IsAdminOrUserViewedMovie
)


# swagger docs 
from drf_yasg.utils import swagger_auto_schema 
from django.utils.decorators import method_decorator 

from rest_framework.decorators import APIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='list all  movie [IsAdminOrReadOnly]',
    operation_description='list all movie [IsAdminOrReadOnly]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='create a movie [IsAdminOrReadOnly]',
    operation_description='create a movie [IsAdminOrReadOnly]',
)) 
class Movie_LC_View(generics.ListCreateAPIView):
    queryset = Movie.objects.all().select_related('moviemedia').prefetch_related('moviemedia__media_files')
    serializer_class = MovieSerializer 
    permission_classes = [IsAdminOrReadOnly]

 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='retrieve particular movie detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='update particular movie detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='patch particular movie detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='delete particular movie detail [IsAdminOrReadOnly]',
))
class Movie_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all().select_related('moviemedia').prefetch_related('moviemedia__media_files')
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='list all movie general detail [IsAdminOrReadOnly]',
    operation_description='list all movie general detail [IsAdminOrReadOnly]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='create a movie general detail [IsAdminOrReadOnly]',
    operation_description='create a movie general detail [IsAdminOrReadOnly]',
))  
class MovieGeneralDetail_LC_View(generics.ListCreateAPIView):
    queryset = MovieGeneralDetail.objects.all().select_related('movie')
    serializer_class = MovieGeneralDetailSerializer 
    permission_classes = [IsAdminOrReadOnly]



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='retrieve particular movie general detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='update particular movie general detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='patch particular movie general detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='delete particular movie general detail [IsAdminOrReadOnly]',
))
class MovieGeneralDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieGeneralDetail.objects.all().select_related('movie')
    serializer_class = MovieGeneralDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='list all movie core detail [IsAdminOrReadOnly]',
    operation_description='list all movie core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='create a movie core detail [IsAdminOrReadOnly]',
    operation_description='create a movie core detail [IsAdminOrReadOnly]',
))  
class MovieCoreDetail_LC_View(generics.ListCreateAPIView):
    queryset = MovieCoreDetail.objects.all().select_related('movie')
    serializer_class = MovieCoreDetailSerializer 
    permission_classes = [IsAdminOrReadOnly]



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='retrieve particular movie core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='update particular movie core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='patch particular movie core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='delete particular movie core detail [IsAdminOrReadOnly]',
))
class MovieCoreDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieCoreDetail.objects.all().select_related('movie')
    serializer_class = MovieCoreDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='list all movie  box office  detail [IsAdminOrReadOnly]',
    operation_description='list all movie tech detail [IsAdminOrReadOnly]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='create a movie  box office  detail [IsAdminOrReadOnly]',
    operation_description='create a movie tech detail [IsAdminOrReadOnly]',
))  
class MovieBoxOffice_LC_View(generics.ListCreateAPIView):
    queryset = MovieBoxOffice.objects.all().select_related('movie')
    serializer_class = MovieBoxOfficeSerializer 
    permission_classes = [IsAdminOrReadOnly]



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='retrieve particular movie box office detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='update particular movie  box office  detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='patch particular movie  box office  detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='delete particular movie  box office  detail [IsAdminOrReadOnly]',
))
class MovieBoxOffice_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieBoxOffice.objects.all().select_related('movie')
    serializer_class = MovieBoxOfficeSerializer 
    permission_classes = [IsAdminOrReadOnly]




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='list all movie tech detail [IsAdminOrReadOnly]',
    operation_description='list all movie tech detail [IsAdminOrReadOnly]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='create a movie tech detail [IsAdminOrReadOnly]',
    operation_description='create a movie tech detail [IsAdminOrReadOnly]',
))  
class MovieTechSpecs_LC_View(generics.ListCreateAPIView):
    queryset = MovieTechSpecs.objects.all().select_related('movie')
    serializer_class = MovieTechSpecsSerializer 
    permission_classes = [IsAdminOrReadOnly]




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='retrieve particular movie tech detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='update particular movie tech detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='patch particular movie tech detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='delete particular movie tech detail [IsAdminOrReadOnly]',
))
class MovieTechSpecs_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieTechSpecs.objects.all().select_related('movie')
    serializer_class = MovieTechSpecsSerializer 
    permission_classes = [IsAdminOrReadOnly]



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='list all movie review [AllowAny] [Paginate-10]',
    operation_description='list all movie review [AllowAny] [Paginate-10]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='create a movie review [IsAuthenticated]',
    operation_description='create a movie review [IsAuthenticated]',
))  
class MovieRatingReview_LC_View(generics.ListCreateAPIView):
    queryset = MovieRatingReview.objects.all().select_related('movie')
    serializer_class = MovieRatingReviewSerializer
    pagination_class = GlobalPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny]  # Anyone can view
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated]  # Custom permission
        return super().get_permissions()




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='retrieve particular movie review [AllowAny] ',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='update particular movie review [IsMovieReviewer_OrReadOnly] ',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='patch particular movie review [IsMovieReviewer_OrReadOnly] ',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='delete particular movie review [IsMovieReviewer_OrReadOnly] ',
))
class MovieRatingReview_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieRatingReview.objects.all().select_related('movie')
    serializer_class = MovieRatingReviewSerializer
    permission_classes = [IsMovieReviewer_OrReadOnly] 



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieUserVotes APIs'], operation_id='list all movie votes [AllowAny]',
    operation_description='list all movie votes [AllowAny]',
))
class MovieVotes_List_View(generics.ListAPIView):
    queryset = MovieVotes.objects.all().select_related('movie')
    serializer_class = MovieVotesSerializer




@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieUserVotes APIs'], operation_id='give vote on movie [IsMovieVoter_OrReadOnly]',
    operation_description='give vote on movie [IsMovieVoter_OrReadOnly]',
)) 
@permission_classes([permissions.IsAuthenticated])
class UserMovieVotesToggleView(generics.CreateAPIView):
    serializer_class = MovieVotesSerializer
    permission_classes = [IsMovieVoter_OrReadOnly]

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
    tags=['App6 : MovieUserWatchlist APIs'], operation_id='list all user watchlist [IsAdminOrUserWatchlistedMovie] [Paginate-10]',
    operation_description='list all user watchlist [IsAuthenticated] [Paginate-10]',
))
class UserMovieWatchlist_List_View(generics.ListAPIView):
    queryset = UserMovieWatchlist.objects.all().select_related('movie')
    serializer_class = UserMovieWatchlistSerializer
    permission_classes = [IsAdminOrUserWatchlistedMovie]
    pagination_class = GlobalPagination



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieUserWatchlist APIs'], operation_id='create a user watchlist [IsUserMovieWatchlist_OrReadOnly]',
    operation_description='create a user watchlist [IsUserMovieWatchlist_OrReadOnly]',
)) 
@permission_classes([permissions.IsAuthenticated])
class UserMovieWatchlistToggleView(generics.CreateAPIView):
    serializer_class = UserMovieWatchlistSerializer
    permission_classes = [IsUserMovieWatchlist_OrReadOnly]

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
    tags=['App6 : MovieUserViewed APIs'], operation_id='list all user viewing list [IsAdminOrUserViewedMovie] [Paginate-10]',
    operation_description='list all user viewing list [IsAdminOrUserViewedMovie]',
))
class UserMovieViewed_List_View(generics.ListAPIView):
    queryset = UserMovieViewed.objects.all().select_related('movie')
    serializer_class = UserMovieViewedSerializer
    permission_classes = [IsAdminOrUserViewedMovie]
    pagination_class = GlobalPagination


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieUserViewed APIs'], operation_id='create a user viewing history [IsUserViewedMovie_OrReadOnly]',
    operation_description='create a user viewing history [IsUserViewedMovie_OrReadOnly]',
)) 
@permission_classes([permissions.IsAuthenticated])
class UserMovieViewedToggleView(generics.CreateAPIView):
    serializer_class = UserMovieViewedSerializer
    permission_classes = [IsUserViewedMovie_OrReadOnly]

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


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieHistory APIs'], operation_id='create a user history [IsAuthenticated]',
    operation_description='create a user history [IsAuthenticated]',
)) 
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieHistory APIs'], operation_id='create a user history [IsAuthenticated] [Paginate-10]',
    operation_description='create a user history',
)) 
class MovieWatchHistoryView(generics.ListCreateAPIView):
    queryset = MovieWatchHistory.objects.all()
    serializer_class = MovieWatchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = GlobalPagination

