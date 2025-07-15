from app1_media_manger.models import MovieMedia, TVShowMedia, EpisodeMedia, SeasonMedia, CastMedia, CreatorMedia, WriterMedia,  MediaFile
from .serializers import ( 
    MediaFileSerializer,
    MovieSerializerWithMedia, TVShowSerializerWithMedia, SeasonSerializerWithMedia, EpisodeSerializerWithMedia, 

    CastCreateSerializer, CastSerializerWithMedia,CreatorSerializerWithMedia, WriterSerializerWithMedia , CreatorCreateSerializer, WriterCreateSerializer, MovieCreateSerializer, 
    TVShowCreateSerializer, SeasonCreateSerializer, EpisodeCreateSerializer
)


from rest_framework import generics
from django.contrib.contenttypes.models import ContentType
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status
from rest_framework.response import Response

#swagger docs
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator


#custom permissions 
from shared.permissions import IsAdminOrReadOnly 
from rest_framework import permissions


#custom Pagination
from rest_framework import pagination
from shared.pagination import GlobalPagination

# db optimization 
from django.db.models import Prefetch

'''
✅  When should you use two serializers?
    : Use two serializers when:
        - Your input fields ≠ model fields (custom logic, nested creation).
        - Your output needs extra/related data (like media_files, IDs, etc.).
        - You want to keep logic clean and separated.

✅ When should you use only one serializer?
    : Use one serializer when:
        - Your input fields match the model fields directly.
        - You don't need special logic for create and read operation.
        - The output structure is simple (no nested relationships or computed fields).
        - You want to keep the codebase minimal and avoid duplication.
        - You're doing basic CRUD operations with no major difference between input and output.

'''



# MediaFile views
# -----------------------------------------------------------------------------------------
class MediaFileList(generics.ListCreateAPIView):
    queryset = MediaFile.objects.select_related('content_type').all()
    serializer_class = MediaFileSerializer
    pagination_class = GlobalPagination
    permission_classes = [IsAdminOrReadOnly]

class MediaFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return MediaFile.objects.select_related('content_type').all()
    

# GET- Fetch , POST Create : Views with media handling 
# -----------------------------------------------------------------------------------------

# For listing all movie entries with media
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : MovieMedia APIs'], operation_id='get all movie with media [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='get all movie with media [IsAdminOrReadOnly] [Paginate-10]',
))
class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializerWithMedia
    pagination_class = GlobalPagination
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = MovieMedia.objects.prefetch_related(
                'media_files',
        )
        return queryset


# For creating single movie entry
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : MovieMedia APIs'], operation_id='create single movie with media [IsAdminOrReadOnly]',
    operation_description='create single movie with media [IsAdminOrReadOnly]',
))
class MovieCreateView(generics.CreateAPIView):
    serializer_class = MovieCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser] # need MultiPartParser for file uploads and JSONParser for regular API calls

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list) # Bulk creation allowed 
        serializer = self.get_serializer(data=request.data,  many=many)
        serializer.is_valid(raise_exception=True)
        movies = serializer.save()

        # prefetch media_files and content_type to avoid N+1 queries
        if many:
            movie_qs = MovieMedia.objects.prefetch_related('media_files').filter(
                id_in = [m.id for m in movies]
            )
        else:
            movie_qs = MovieMedia.objects.prefetch_related('media_files').get(
                id=movies.id
            )
        output_serializer = MovieSerializerWithMedia(movie_qs, many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

 
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : MovieMedia APIs'], operation_id='retrieve particular movie detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['📽️ App1 : MovieMedia APIs'], operation_id='update particular movie detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['📽️ App1 : MovieMedia APIs'], operation_id='patch particular movie detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['📽️ App1 : MovieMedia APIs'], operation_id='delete particular movie detail [IsAdminOrReadOnly]',
))
class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        return MovieMedia.objects.prefetch_related('media_files').all()
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = MovieSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        movie = serializer.save()

        # Refetch with media files for output
        movie_with_media = MovieMedia.objects.prefetch_related(
            'media_files'
        ).get(id=movie.id)

        output_serializer = MovieSerializerWithMedia(movie_with_media)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Use partial=True for patch
        serializer.is_valid(raise_exception=True)
        movie = serializer.save()

        # Refetch with media files for output
        movie_with_media = MovieMedia.objects.prefetch_related(
            'media_files'
        ).get(id=movie.id)

        output_serializer = MovieSerializerWithMedia(movie_with_media)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'detail': 'Moviemedia deleted successfully.'},status=status.HTTP_204_NO_CONTENT)



# -----------------------------------------------------------------------------------------

# For listing all cast entries with media
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CastMedia APIs'], operation_id='list all cast with media [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all cast with media [IsAdminOrReadOnly] [Paginate-10]',
))
class CastListView(generics.ListAPIView):
    queryset = CastMedia.objects.prefetch_related('media_files').all()
    serializer_class = CastSerializerWithMedia
    pagination_class = GlobalPagination
    permission_classes = [IsAdminOrReadOnly]



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CastMedia APIs'], operation_id='create independent cast with media [IsAdminOrReadOnly]',
    operation_description='create independent cast with media [IsAdminOrReadOnly]',
)) 
class CastCreateView(generics.CreateAPIView):
    serializer_class = CastCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        casts = serializer.save()

        if many: 
            cast_qs = CastMedia.objects.prefetch_related('media_files').filter(
                id___in = [ c.id for c in casts]
            )
        else:
            cast_qs = CastMedia.objects.prefetch_related('media_files').get(
                id = casts.id
            )

        output_serializer = CastSerializerWithMedia(cast_qs, many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CastMedia APIs'], operation_id='retrieve particular caste detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CastMedia APIs'], operation_id='update particular caste detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CastMedia APIs'], operation_id='patch particular caste detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CastMedia APIs'], operation_id='delete particular caste detail [IsAdminOrReadOnly]',
))
class CastDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CastCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        return CastMedia.objects.prefetch_related('media_files').all()
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = CastSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        cast = serializer.save()

        cast_with_media = CastMedia.objects.prefetch_related(
            'media_files'
        ).get(id=cast.id)
        output_serializer = CastSerializerWithMedia(cast_with_media)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# -----------------------------------------------------------------------------------------
# For listing all creator entries with media
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CreatorMedia APIs'], operation_id='list all creator with media [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all creator with media [IsAdminOrReadOnly] [Paginate-10]',
))
class CreatorListView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination
    serializer_class = CreatorSerializerWithMedia

    def get_queryset(self):
        return CreatorMedia.objects.prefetch_related('media_files').all()



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CreatorMedia APIs'], operation_id='create independent creator [IsAdminOrReadOnly]',
    operation_description='create independent creator [IsAdminOrReadOnly]',
))
class CreatorCreateView(generics.CreateAPIView):
    serializer_class = CreatorCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        creators = serializer.save()

        if many:
            creator_qs = CreatorMedia.objects.prefetch_related('media_files').filter(
                id_in = [c.id for c in creators]
            )
        else:
            creator_qs = CreatorMedia.objects.prefetch_related('media_files').get(
                id = creators.id
            )

        output_serializer = CreatorSerializerWithMedia(creator_qs,many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CreatorMedia APIs'], operation_id='retrieve particular creator detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CreatorMedia APIs'], operation_id='update particular creator detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CreatorMedia APIs'], operation_id='patch particular creator detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CreatorMedia APIs'], operation_id='delete particular creator detail [IsAdminOrReadOnly]',
))
class CreatorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreatorCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        return CreatorMedia.objects.prefetch_related(
            'media_files'
        ).all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = CreatorSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        creator = serializer.save()

        creator = CreatorMedia.objects.prefetch_related(
            'media_files'
        ).get(id=creator.id)
        output_serializer = CreatorSerializerWithMedia(creator)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------------------------------

# For listing all Writer entries with media
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : WriterMedia APIs'], operation_id='list all writer with media [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all writer with media [IsAdminOrReadOnly] [Paginate-10]',
))
class WriterListView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination
    serializer_class = WriterSerializerWithMedia

    def get_queryset(self):
        return WriterMedia.objects.prefetch_related('media_files').all()




@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : WriterMedia APIs'], operation_id='create independent writer [IsAdminOrReadOnly]',
    operation_description='create independent writer [IsAdminOrReadOnly]',
))
class WriterCreateView(generics.CreateAPIView):
    queryset = WriterMedia.objects.prefetch_related('media_files').all()
    serializer_class = WriterCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        '''
            # list of WriterMedia instances if many = True
            # single WriterMedia instances if many = False
        '''
        writers = serializer.save() 

        if many:
            writers_qs = WriterMedia.objects.prefetch_related('media_files').filter(
                id__in=[w.id for w in writers]
            )
        else:
            writers_qs = WriterMedia.objects.prefetch_related('media_files').get(
                id=writers.id
            )

        output_serializer = WriterSerializerWithMedia(writers_qs,many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : WriterMedia APIs'], operation_id='retrieve particular writer detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['📽️ App1 : WriterMedia APIs'], operation_id='update particular writer detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['📽️ App1 : WriterMedia APIs'], operation_id='patch particular writer detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['📽️ App1 : WriterMedia APIs'], operation_id='delete particular writer detail [IsAdminOrReadOnly]',
)) 
class WriterDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WriterCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        return WriterMedia.objects.prefetch_related(
            'media_files'
        ).all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = WriterSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        writer = serializer.save()

        writer = WriterMedia.objects.prefetch_related(
            'media_files'
        ).get(id=writer.id)

        output_serializer = WriterSerializerWithMedia(writer)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# -----------------------------------------------------------------------------------------
# For listing all tvshow entries with media
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVShowMedia APIs'], operation_id='list all tvshow with media [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all tvshow with media [IsAdminOrReadOnly] [Paginate-10]',
))
class TvShowListView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination
    serializer_class = TVShowSerializerWithMedia

    def get_queryset(self):
        return TVShowMedia.objects.prefetch_related('media_files').all()


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVShowMedia APIs'], operation_id='create independent tvshow [IsAdminOrReadOnly]',
    operation_description='create independent tvshow [IsAdminOrReadOnly]',
))
class TVShowCreateView(generics.CreateAPIView):
    serializer_class = TVShowCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]


    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        tvshows = serializer.save()

        if many:
            tvshow_qs = TVShowMedia.objects.prefetch_related('media_files').filter(
                id_in = [t.id for t in tvshows]
            )
        else:
            tvshow_qs = TVShowMedia.objects.prefetch_related('media_files').get(
                id = tvshows.id
            )

        output_serializer = TVShowSerializerWithMedia(tvshow_qs , many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVShowMedia APIs'], operation_id='retrieve particular tvshow detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVShowMedia APIs'], operation_id='update particular tvshow detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVShowMedia APIs'], operation_id='patch particular tvshow detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVShowMedia APIs'], operation_id='delete particular tvshow detail [IsAdminOrReadOnly]',
))
class TVShowDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TVShowCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        return TVShowMedia.objects.prefetch_related('media_files').all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = TVShowSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        tvshow = serializer.save()

        tvshow = TVShowMedia.objects.prefetch_related('media_files').get(id = tvshow.id)
        output_serializer = TVShowSerializerWithMedia(tvshow)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# -----------------------------------------------------------------------------------------
# For listing all season entries with media
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='list all season for particular tvshow [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all season for particular tvshow [IsAdminOrReadOnly] [Paginate-10]',
))
class SeasonListView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination
    serializer_class = SeasonSerializerWithMedia

    def get_queryset(self):
        return  SeasonMedia.objects.select_related('tvshow').prefetch_related(
            'media_files'
        )

@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='create season for particular tvshow [IsAdminOrReadOnly]',
    operation_description='create independent tvshow [IsAdminOrReadOnly]',
))
class SeasonCreateView(generics.CreateAPIView):
    serializer_class = SeasonCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        season = serializer.save()

        if many:
            season_qs = SeasonMedia.objects.filter(
                id__in=[s.id for s in season]
            ).select_related('tvshow').prefetch_related('media_files')
        else:
            season_qs = SeasonMedia.objects.select_related(
                'tvshow'
            ).prefetch_related('media_files').filter(id=season.id)

        output_serializer = SeasonSerializerWithMedia(season_qs , many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='retrieve particular season detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='update particular season detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='patch particular season detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='delete particular season detail [IsAdminOrReadOnly]',
))
class SeasonDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = SeasonCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        return SeasonMedia.objects.select_related(
            'tvshow'
        ).prefetch_related('media_files').all()
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = SeasonSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        season = serializer.save()

        season = SeasonMedia.objects.select_related(
            'tvshow'
        ).prefetch_related('media_files').get(id=season.id)

        output_serializer = SeasonSerializerWithMedia(season)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------------------------------

# For listing all episode entries with media
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='list all episode with media [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all episode with media [IsAdminOrReadOnly] [Paginate-10]',
))
class EpisodeListView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination
    serializer_class = EpisodeSerializerWithMedia

    def get_queryset(self):
        return EpisodeMedia.objects.select_related('tvshow', 'season').prefetch_related('media_files').all()


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='create episode for particular season [IsAdminOrReadOnly]',
    operation_description='create episode for particular season [IsAdminOrReadOnly]',
))
class EpisodeCreateView(generics.CreateAPIView):
    serializer_class = EpisodeCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        episodes = serializer.save()

        # If many=True, episodes is a list; otherwise a single instance
        if many:
            episodes_qs = EpisodeMedia.objects.filter(id__in=[ep.id for ep in episodes]) \
                .select_related('tvshow', 'season') \
                .prefetch_related('media_files')
            output_serializer = EpisodeSerializerWithMedia(episodes_qs, many=True)
        else:
            episode_qs = EpisodeMedia.objects.select_related('tvshow', 'season') \
                .prefetch_related('media_files') \
                .get(id=episodes.id)
            output_serializer = EpisodeSerializerWithMedia(episode_qs)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    

@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='retrieve particular episode detail [IsAdminOrReadOnly]',
)) 
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='update particular episode detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='patch particular episode detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='delete particular episode detail [IsAdminOrReadOnly]',
))
class EpisodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EpisodeCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        return EpisodeMedia.objects.select_related('tvshow', 'season').prefetch_related('media_files').all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = EpisodeSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        episode = serializer.save()

        episode = EpisodeMedia.objects.select_related('tvshow', 'season').prefetch_related('media_files').get(id=episode.id)
        output_serializer = EpisodeSerializerWithMedia(episode)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------------------------------------------------

