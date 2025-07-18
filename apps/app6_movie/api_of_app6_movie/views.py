# views.py
from app6_movie.models import  ( 
    Movie, MovieGeneralDetail , MovieCoreDetail, 
    MovieBoxOffice, MovieTechSpecs, MovieRatingReview,
    UserMovieWatchlist, UserMovieViewed, MovieVotes, MovieWatchHistory
)

from app1_media_manger.models import MediaFile

from .serializers import  (
    MovieReadSerializer, MovieWriteSerializer, 
    MovieGenralDetail_ReadSerializer,MovieGenralDetail_ReadSerializer,

    MovieCoreDetail_ReadSerializer, MovieCoreDetail_WriteSerializer,
    MovieBoxOffice_ReadSerializer, MovieBoxOffice_WriteSerializer,
    
    MovieGeneralDetail_WriteSerializer, MovieGeneralDetail_WriteSerializer,
    MovieTechSpecs_ReadSerializer, MovieTechSpecs_WriteSerializer,
    MovieRatingReview_ReadSerializer, MovieRatingReview_WriteSerializer,

    MovieVotes_ReadSerializer, MovieVotes_WriteSerializer,
    UserMovieWatchlistSerializer, UserMovieViewedSerializer,
    MovieWatchHistory_ReadSerializer, MovieWatchHistory_WriteSerializer,

    MovieDetailSerializer, LightMovieSerializer
)

from rest_framework import generics , status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser

#pagination 
from rest_framework import pagination
from rest_framework.decorators import permission_classes
from shared.pagination import GlobalPagination

#caching
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

#permissions
from rest_framework import permissions
from shared.permissions import IsAdminOrReadOnly
from .custom_permission import  ( 
    IsMovieReviewer_OrReadOnly, IsMovieVoter_OrReadOnly, 
    IsUserMovieWatchlist_OrReadOnly,IsAdminOrUserWatchlistedMovie,
    IsUserViewedMovie_OrReadOnly, IsAdminOrUserViewedMovie
)
 
from django.db.models import Prefetch 

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
class MovieListView(generics.ListAPIView):
    serializer_class = MovieReadSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination

    def get_queryset(self):
        return Movie.objects.select_related(
            'moviemedia',
            'platform',
        ).prefetch_related(
            'movie_genre',
            'movie_cast',
            'movie_creator',
            'movie_writer',
            'moviemedia__media_files'
        )


# Nothing is returned : only creates 
# class MovieCreateView(generics.CreateAPIView):
#     serializer_class = MovieWriteSerializer
#     permission_classes = [IsAdminOrReadOnly]

@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : Movie APIs'], operation_id='create a movie [IsAdminOrReadOnly]',
    operation_description='create a movie [IsAdminOrReadOnly]',
)) 
# creates with one serializer and gives output from another serializer with media rich content
class MovieCreateView(generics.CreateAPIView):
    serializer_class = MovieWriteSerializer
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list) # bulk creation allowed
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        movies = serializer.save() 

        # prefetch media_files and content_type to avoid N+1 queries
        if many:
            movie_qs = Movie.objects.prefetch_related('moviemedia__media_files').filter(
                id__in=[m.id for m in movies]
            )
        else:
            movie_qs = Movie.objects.prefetch_related('moviemedia__media_files').get(
                id=movies.id
            )
        output_serializer = MovieReadSerializer(movie_qs, many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    



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
    serializer_class = MovieReadSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]
    http_method_names = ['get', 'put', 'patch', 'delete']
    lookup_field = 'pk'  # Default lookup field is 'id', can be changed if needed
 
    def get_queryset(self):
        return Movie.objects.select_related('moviemedia').prefetch_related('moviemedia__media_files')
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MovieWriteSerializer
        return MovieReadSerializer
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object() # by_default uses lookup_field 'id' to get the instance
        output_serializer = self.get_serializer(instance) 
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object() #get model instance
        serializer = self.get_serializer(instance, data=request.data, partial=False) #combine instance + parsed input data
        serializer.is_valid(raise_exception=True) #validate the data
        serializer.save() #save the data
        
        # Re-fetch with media files for output 
        movie_with_media = Movie.objects.select_related('moviemedia').prefetch_related(
            'moviemedia__media_files'
        ).get(id=instance.id)

        output_serializer = MovieReadSerializer(movie_with_media) #serialize the output
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object() #get model instance
        serializer = self.get_serializer(instance, data=request.data, partial=True) #combine instance + parsed input data
        serializer.is_valid(raise_exception=True) #validate the data
        serializer.save() #save the data
        
        # Re-fetch with media files for output 
        movie_with_media = Movie.objects.select_related('moviemedia').prefetch_related(
            'moviemedia__media_files'
        ).get(id=instance.id)

        output_serializer = MovieReadSerializer(movie_with_media) #serialize the output
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object() #get model instance
        instance.delete() #delete the instance
        return Response({'detail': 'Movie deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='list all movie general detail [IsAdminOrReadOnly]',
    operation_description='list all movie general detail [IsAdminOrReadOnly]',
)) 
class MovieGeneralDetail_L_View(generics.ListAPIView):
    serializer_class = MovieGenralDetail_ReadSerializer 
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return MovieGeneralDetail.objects.select_related('movie', 'movie__moviemedia')




@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieGeneralDetail APIs'], operation_id='create a movie general detail [IsAdminOrReadOnly]',
    operation_description='create a movie general detail [IsAdminOrReadOnly]',
)) 
class MovieGeneralDetail_C_View(generics.CreateAPIView):
    serializer_class = MovieGeneralDetail_WriteSerializer 
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list) # returns either True or False.
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        movie_general_details = serializer.save() 

        # prefetch media_files and content_type to avoid N+1 queries
        if many:
            '''
                Notes: 
                 - MovieGeneralDetail.objects.(..operations ..) = [<MovieGeneralDetail: id=1>, <MovieGeneralDetail: id=2>, ...]
                    - eg : movie_general_details.id = 1
                    - returns : <MovieGeneralDetail: id=1>

                -  [m.id for m in movie_general_details]
                    - returns :  [1, 2, ...]

                -  “From the MovieGeneralDetail table, get all rows whose IDs match the 
                    list movie_general_details, and while doing that, also preload the 
                    related movie (foreign key) for each row — in a single query.”
            
            '''
            many_ids = [m.id for m in movie_general_details]
            moviegeneraldetail_qs = MovieGeneralDetail.objects.select_related('movie').filter(
                id__in=many_ids
            )
        else:
            single_id = movie_general_details.id
            moviegeneraldetail_qs = MovieGeneralDetail.objects.select_related('movie').get(
                id=single_id
            )

        output_serializer = MovieGenralDetail_ReadSerializer(moviegeneraldetail_qs, many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)



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
    serializer_class = MovieGenralDetail_ReadSerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get', 'put', 'patch', 'delete']
    lookup_field = 'pk'  # Default lookup field is 'id', can be changed if needed

    def get_queryset(self):
        return MovieGeneralDetail.objects.select_related('movie', 'movie__moviemedia')
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MovieGeneralDetail_WriteSerializer
        return MovieGenralDetail_ReadSerializer
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object() # fetch model instance
        output_serializer = self.get_serializer(instance) # model instance to serializer
        return Response(output_serializer.data) # return json response
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object() # fetch model instance
        serializer = self.get_serializer(instance, data=request.data, partial=False) # combine instance + parsed input data
        serializer.is_valid(raise_exception=True) # validate the data
        serializer.save() # save the data
        
        # Re-fetch with media files for output
        movie_general_detail = MovieGeneralDetail.objects.select_related(
            'movie'
        ).get(id=instance.id)
        output_serializer = MovieGenralDetail_ReadSerializer(movie_general_detail) # serialize the output
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object() # fetch model instance
        serializer = self.get_serializer(instance, data=request.data, partial=True) # combine instance + parsed input data
        serializer.is_valid(raise_exception=True) # validate the data
        serializer.save() # save the data
        
        # Re-fetch with media files for output
        movie_general_detail = MovieGeneralDetail.objects.select_related(
            'movie'
        ).get(id=instance.id)
        output_serializer = MovieGenralDetail_ReadSerializer(movie_general_detail) # serialize the output
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()  # delete the instance
        return Response({'detail': 'Movie general detail deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='list all movie core detail [IsAdminOrReadOnly]',
    operation_description='list all movie core detail [IsAdminOrReadOnly]',
))
class MovieCoreDetail_L_View(generics.ListAPIView):
    queryset = MovieCoreDetail.objects.select_related('movie', 'movie__moviemedia').prefetch_related('language', 'production_companies').all()
    serializer_class = MovieCoreDetail_ReadSerializer 
    permission_classes = [IsAdminOrReadOnly]



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieCoreDetail APIs'], operation_id='create a movie core detail [IsAdminOrReadOnly]',
    operation_description='create a movie core detail [IsAdminOrReadOnly]',
))  
class MovieCoreDetail_C_View(generics.CreateAPIView):
    serializer_class =  MovieCoreDetail_WriteSerializer
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list) # returns either True or False.
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        movie_core_details = serializer.save() 

        # prefetch media_files and content_type to avoid N+1 queries
        if many:
            many_ids = [m.id for m in movie_core_details]
            moviecoredetail_qs = MovieCoreDetail.objects.select_related('movie', 'movie__moviemedia').filter(
                id__in=many_ids
            )
        else:
            single_id = movie_core_details.id
            moviecoredetail_qs = MovieCoreDetail.objects.select_related('movie', 'movie__moviemedia').get(
                id=single_id
            )

        output_serializer = MovieCoreDetail_ReadSerializer(moviecoredetail_qs, many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)




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
    serializer_class = MovieCoreDetail_ReadSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return MovieCoreDetail.objects.all().select_related('movie', 'movie__moviemedia')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MovieCoreDetail_WriteSerializer
        return MovieCoreDetail_ReadSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object() 
        output_serializer = self.get_serializer(instance)
        return Response(output_serializer.data)
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save() 

        # Re-fetch with media files for output
        movie_core_detail = MovieCoreDetail.objects.select_related(
            'movie'
        ).get(id=instance.id)
        output_serializer = MovieCoreDetail_ReadSerializer(movie_core_detail)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save() 

        # Re-fetch with media files for output
        movie_core_detail = MovieCoreDetail.objects.select_related(
            'movie'
        ).get(id=instance.id)
        output_serializer = MovieCoreDetail_ReadSerializer(movie_core_detail)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'detail': 'Movie core detail deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='list all movie  box office  detail [IsAdminOrReadOnly]',
    operation_description='list all movie tech detail [IsAdminOrReadOnly]',
))
class MovieBoxOffice_L_View(generics.ListAPIView):
    queryset = MovieBoxOffice.objects.select_related('movie', 'movie__moviemedia')
    serializer_class = MovieBoxOffice_ReadSerializer 
    permission_classes = [IsAdminOrReadOnly]


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieBoxOffice APIs'], operation_id='create a movie  box office  detail [IsAdminOrReadOnly]',
    operation_description='create a movie tech detail [IsAdminOrReadOnly]',
))  
class MovieBoxOffice_C_View(generics.CreateAPIView):
    serializer_class = MovieBoxOffice_WriteSerializer
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        movie_box_offices = serializer.save()
        # prefetch media_files and content_type to avoid N+1 queries
        if many:
            many_ids = [m.id for m in movie_box_offices]
            movieboxoffice_qs = MovieBoxOffice.objects.select_related('movie', 'movie__moviemedia').filter(
                id__in=many_ids
            )
        else:
            single_id = movie_box_offices.id
            movieboxoffice_qs = MovieBoxOffice.objects.select_related('movie','movie__moviemedia').get(
                id=single_id
            )
        output_serializer = MovieBoxOffice_ReadSerializer(movieboxoffice_qs, many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    



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
    serializer_class = MovieBoxOffice_ReadSerializer 
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return MovieBoxOffice.objects.select_related('movie', 'movie__moviemedia')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MovieBoxOffice_WriteSerializer
        return MovieBoxOffice_ReadSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = self.get_serializer(instance)
        return Response(output_serializer.data)
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save() 

        # Re-fetch with media files for output
        movie_box_office = MovieBoxOffice.objects.select_related(
            'movie', 'movie__moviemedia'
        ).get(id=instance.id)
        output_serializer = MovieBoxOffice_ReadSerializer(movie_box_office)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):  
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save() 

        # Re-fetch with media files for output
        movie_box_office = MovieBoxOffice.objects.select_related(
            'movie', 'movie__moviemedia'
        ).get(id=instance.id)
        output_serializer = MovieBoxOffice_ReadSerializer(movie_box_office)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'detail': 'Movie box office detail deleted successfully.'}, status=status.HTTP_204_NO_CONTENT) 




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='list all movie tech detail [IsAdminOrReadOnly]',
    operation_description='list all movie tech detail [IsAdminOrReadOnly]',
))
class MovieTechSpecs_L_View(generics.ListAPIView):
    queryset = MovieTechSpecs.objects.select_related('movie', 'movie__moviemedia')
    serializer_class = MovieTechSpecs_ReadSerializer 
    permission_classes = [IsAdminOrReadOnly]

@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieTechSpecs APIs'], operation_id='create a movie tech detail [IsAdminOrReadOnly]',
    operation_description='create a movie tech detail [IsAdminOrReadOnly]',
))  
class MovieTechSpecs_C_View(generics.CreateAPIView):
    serializer_class = MovieTechSpecs_WriteSerializer 
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return MovieTechSpecs.objects.select_related('movie', 'movie__moviemedia')
    
    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        movie_tech_specs = serializer.save()

        # prefetch media_files and content_type to avoid N+1 queries
        if many:
            many_ids = [m.id for m in movie_tech_specs]
            movietechspecs_qs = MovieTechSpecs.objects.select_related('movie', 'movie__moviemedia').filter(
                id__in=many_ids
            )
        else:
            single_id = movie_tech_specs.id
            movietechspecs_qs = MovieTechSpecs.objects.select_related('movie', 'movie__moviemedia').get(
                id=single_id
            )
        output_serializer = MovieTechSpecs_ReadSerializer(movietechspecs_qs, many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)



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
    serializer_class = MovieTechSpecs_ReadSerializer 
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return MovieTechSpecs.objects.select_related('movie', 'movie__moviemedia')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MovieTechSpecs_WriteSerializer
        return MovieTechSpecs_ReadSerializer
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = self.get_serializer(instance)
        return Response(output_serializer.data)
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save() 

        # Re-fetch with media files for output
        movie_tech_specs = MovieTechSpecs.objects.select_related(
            'movie', 'movie__moviemedia'
        ).get(id=instance.id)
        output_serializer = MovieTechSpecs_ReadSerializer(movie_tech_specs)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save() 

        # Re-fetch with media files for output
        movie_tech_specs = MovieTechSpecs.objects.select_related(
            'movie', 'movie__moviemedia'
        ).get(id=instance.id)
        output_serializer = MovieTechSpecs_ReadSerializer(movie_tech_specs)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'detail': 'Movie tech specs detail deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='list all movie review [AllowAny] [Paginate-10]',
    operation_description='list all movie review [AllowAny] [Paginate-10]',
))

class MovieRatingReview_L_View(generics.ListAPIView):
    queryset = MovieRatingReview.objects.select_related('movie', 'movie__moviemedia').prefetch_related('user_movie_review')
    serializer_class = MovieRatingReview_ReadSerializer
    pagination_class = GlobalPagination


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieRatingReview APIs'], operation_id='create a movie review [IsAuthenticated]',
    operation_description='create a movie review [IsAuthenticated]',
))  
class MovieRatingReview_C_View(generics.CreateAPIView):
    serializer_class = MovieRatingReview_WriteSerializer
    pagination_class = GlobalPagination
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        movie_rating_reviews = serializer.save()
        # prefetch media_files and content_type to avoid N+1 queries
        if many:
            many_ids = [m.id for m in movie_rating_reviews]
            movieratingreview_qs = MovieRatingReview.objects.select_related('movie', 'movie__moviemedia').filter(
                id__in=many_ids
            )
        else:
            single_id = movie_rating_reviews.id
            movieratingreview_qs = MovieRatingReview.objects.select_related('movie', 'movie__moviemedia').get(
                id=single_id
            )
        output_serializer = MovieRatingReview_ReadSerializer(movieratingreview_qs, many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    


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
    serializer_class = MovieRatingReview_ReadSerializer
    permission_classes = [IsMovieReviewer_OrReadOnly] 

    def get_queryset(self):
        return MovieRatingReview.objects.select_related('movie', 'movie__moviemedia')
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MovieRatingReview_WriteSerializer
        return MovieRatingReview_ReadSerializer
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = self.get_serializer(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Re-fetch with media files for output
        movie_rating_review = MovieRatingReview.objects.select_related(
            'movie', 'movie__moviemedia'
        ).get(id=instance.id)
        output_serializer = MovieRatingReview_ReadSerializer(movie_rating_review)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Re-fetch with media files for output
        movie_rating_review = MovieRatingReview.objects.select_related(
            'movie', 'movie__moviemedia'
        ).get(id=instance.id)
        output_serializer = MovieRatingReview_ReadSerializer(movie_rating_review)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'detail': 'Movie review deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : MovieUserVotes APIs'], operation_id='list all movie votes [AllowAny]',
    operation_description='list all movie votes [AllowAny]',
))
class MovieVotes_List_View(generics.ListAPIView):
    queryset = MovieVotes.objects.select_related('movie', 'user_vote')
    serializer_class = MovieVotes_ReadSerializer
    permission_classes = [permissions.AllowAny]




@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : MovieUserVotes APIs'], operation_id='give vote on movie [IsMovieVoter_OrReadOnly]',
    operation_description='give vote on movie [IsMovieVoter_OrReadOnly]',
)) 
@permission_classes([permissions.IsAuthenticated])
class UserMovieVotesToggleView(generics.CreateAPIView):
    serializer_class = MovieVotes_WriteSerializer
    permission_classes = [IsMovieVoter_OrReadOnly]

    def post(self, request, *args, **kwargs):
        user = request.user
        movie_id = request.data.get('movie_id')

        # Check for existing entry
        existing = MovieVotes.objects.filter(user_vote=user, movie_id=movie_id).first()

        if existing:
            existing.delete()
            return Response({'detail': 'Vote removed'}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data={**request.data, 'movie_id': movie_id})
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


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App6 : Movie User History APIs'], operation_id='list a user history [IsAuthenticated]',
    operation_description='list a user history [IsAuthenticated]',
)) 
class MovieWatchHistory_L_View(generics.ListAPIView):
    queryset = MovieWatchHistory.objects.select_related('movie', 'movie__moviemedia')
    serializer_class = MovieWatchHistory_ReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = GlobalPagination


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App6 : Movie User History APIs'], operation_id='create a user history [IsAuthenticated] [Paginate-10]',
    operation_description='create a user history',
)) 
class MovieWatchHistory_C_View(generics.CreateAPIView):
    serializer_class = MovieWatchHistory_WriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = GlobalPagination

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        movie_watch_histories = serializer.save()
        # prefetch media_files and content_type to avoid N+1 queries
        if many:
            many_ids = [m.id for m in movie_watch_histories]
            moviewatchhistory_qs = MovieWatchHistory.objects.select_related('movie', 'movie__moviemedia').filter(
                id__in=many_ids
            )
        else:
            single_id = movie_watch_histories.id
            moviewatchhistory_qs = MovieWatchHistory.objects.select_related('movie', 'movie__moviemedia').get(
                id=single_id  
            )
        output_serializer = MovieWatchHistory_ReadSerializer(moviewatchhistory_qs, many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

 
'''
 getMovieDetail: async (movieId) => {
    try {
      const response = await api.get(`${endpoints.movieDetail}${movieId}/`)
      const movie = response.data
      return {
        id: movie.id,
        title: movie.movie_name,
        year: movie.release_year,
        rating: movie.content_rating || "Not Rated",
        duration: movie.duration,
        genres: movie.genres || [],
        imdbRating: movie.avg_rating,
        ratingCount: movie.rating_count || "0",
        poster: movie.thumbnails[0]?.cdn_url || "/placeholder.svg",
        backdrop: movie.thumbnails[1]?.cdn_url || movie.thumbnails[0]?.cdn_url || "/placeholder.svg",
        plot: movie.plot || "",
        director: movie.director || "Unknown",
        writers: movie.writers || [],
        stars: movie.cast?.slice(0, 3).map((c) => c.cast_name) || [],
        releaseDate: movie.release_date || "",
        country: movie.country || "",
        language: movie.language || "",
        awards: movie.awards || "",
        cast:
          movie.cast?.map((c) => ({
            id: c.id,
            name: c.cast_name,
            character: c.character || "",
            image: c.profile_pic[0]?.cdn_url || "/placeholder.svg",
          })) || [],
        crew:
          movie.crew?.map((c) => ({
            id: c.id,
            name: c.name,
            job: c.job,
            image: c.profile_pic || "/placeholder.svg",
          })) || [],
        photos: movie.thumbnails?.map((t) => t.cdn_url) || [],
        videos: movie.videos || [],
        reviews: movie.reviews || [],
        technicalSpecs: {
          runtime: movie.duration || "",
          aspectRatio: movie.aspect_ratio || "16:9",
          soundMix: movie.sound_mix || "Dolby Digital",
          color: movie.color || "Color",
        },
      }
    } catch (error) {
      console.error("Failed to fetch movie detail:", error)
      throw error
    }
  },
 
 '''


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['Collector Engine '], operation_id='fetch Movie detail [Paginate-10]',
    operation_description='fetch Movie detail ',
)) 
class MovieDetail(generics.RetrieveAPIView):
    serializer_class = MovieDetailSerializer
    lookup_field = 'pk'  # or 'id' if using UUIDs

    @method_decorator(cache_page(60 * 60))  # Cache for 1 hour
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return (
            Movie.objects
            .select_related(
                'moviemedia',                     # OneToOne
                'movie_general_detail',           # OneToOne
                'movie_core_detail',              # OneToOne
                # 'movie_box_office',               # OneToOne
                'movie_tech_specs',               # OneToOne
                'platform',                       # ForeignKey
            )
            .prefetch_related(
                'movie_genre',                    # M2M
                'movie_cast',    
                # 'movie_cast__profile_pic',        # M2M + related images
                'movie_creator',                  # M2M
                'movie_writer',                   # M2M
                'movie_core_detail__language',    # M2M inside OneToOne
                'movie_core_detail__production_companies',  # M2M inside OneToOne
                'moviemedia__media_files',        # Reverse FK from media
                'movie_reviews__user_movie_review',  # Reverse FK + user
            ).only(
                'id',
                'moviemedia__name',
                'moviemedia__id',
                'platform__platform',
                'movie_general_detail__avg_rating',
                'movie_general_detail__number_rating',
                'movie_general_detail__duration',
                'movie_general_detail__storyline',
                'movie_reviews__rating',
                'movie_core_detail__release_date',
                'movie_tech_specs__runtime',
                'movie_tech_specs__sound_mix',
                'movie_tech_specs__color',
            )
        )