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

'''
✅  When should you use two serializers?
    : Use two serializers when:
        - Your input fields ≠ model fields (custom logic, nested creation).
        - Your output needs extra/related data (like media_files, IDs, etc.).
        - You want to keep logic clean and separated.
'''



# MediaFile views
# -----------------------------------------------------------------------------------------
class MediaFileList(generics.ListCreateAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    pagination_class = GlobalPagination
    permission_classes = [IsAdminOrReadOnly]

class MediaFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = [IsAdminOrReadOnly]



class BaseMediaView:
    """Base view for handling media prefetching"""
    def get_object(self):
        obj = super().get_object()
        content_type = ContentType.objects.get_for_model(obj)
        obj.media_files_prefetched = MediaFile.objects.filter(
            content_type=content_type,
            object_id=obj.id
        )
        return obj



# GET- Fetch , POST Create : Views with media handling 
# -----------------------------------------------------------------------------------------

# For listing all movie entries with media
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : MovieMedia APIs'], operation_id='get all movie with media [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='get all movie with media [IsAdminOrReadOnly] [Paginate-10]',
))
class MovieListView(generics.ListAPIView):
    queryset = MovieMedia.objects.all()
    serializer_class = MovieSerializerWithMedia
    pagination_class = GlobalPagination
    permission_classes = [IsAdminOrReadOnly]


# For creating single movie entry
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : MovieMedia APIs'], operation_id='create single movie with media [IsAdminOrReadOnly]',
    operation_description='create single movie with media [IsAdminOrReadOnly]',
))
class MovieCreateView(generics.CreateAPIView):
    queryset = MovieMedia.objects.all()
    serializer_class = MovieCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data,  many=many)
        serializer.is_valid(raise_exception=True)
        movie = serializer.save()

        output_serializer = MovieSerializerWithMedia(movie, many=many)
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
    queryset = MovieMedia.objects.all()
    serializer_class = MovieCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = MovieSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        movie = serializer.save()

        output_serializer = MovieSerializerWithMedia(movie)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# -----------------------------------------------------------------------------------------

# For listing all cast entries with media
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CastMedia APIs'], operation_id='list all cast with media [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all cast with media [IsAdminOrReadOnly] [Paginate-10]',
))
class CastListView(generics.ListAPIView):
    queryset = CastMedia.objects.all()
    serializer_class = CastSerializerWithMedia
    pagination_class = GlobalPagination
    permission_classes = [IsAdminOrReadOnly]



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CastMedia APIs'], operation_id='create independent cast with media [IsAdminOrReadOnly]',
    operation_description='create independent cast with media [IsAdminOrReadOnly]',
)) 
class CastCreateView(generics.CreateAPIView):
    queryset = CastMedia.objects.all()
    serializer_class = CastCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        cast = serializer.save()

        output_serializer = CastSerializerWithMedia(cast, many=many)
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
    queryset = CastMedia.objects.all()
    serializer_class = CastCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = CastSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        cast = serializer.save()
        output_serializer = CastSerializerWithMedia(cast)
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
    queryset = CreatorMedia.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination
    serializer_class = CreatorSerializerWithMedia



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : CreatorMedia APIs'], operation_id='create independent creator [IsAdminOrReadOnly]',
    operation_description='create independent creator [IsAdminOrReadOnly]',
))
class CreatorCreateView(generics.CreateAPIView):
    queryset = CreatorMedia.objects.all()
    serializer_class = CreatorCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        creator = serializer.save()
        output_serializer = CreatorSerializerWithMedia(creator,many=many)
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
    queryset = CreatorMedia.objects.all()
    serializer_class = CreatorCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = CreatorSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        creator = serializer.save()
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
    queryset = WriterMedia.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination
    serializer_class = WriterSerializerWithMedia




@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : WriterMedia APIs'], operation_id='create independent writer [IsAdminOrReadOnly]',
    operation_description='create independent writer [IsAdminOrReadOnly]',
))
class WriterCreateView(generics.CreateAPIView):
    queryset = WriterMedia.objects.all()
    serializer_class = WriterCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        writer = serializer.save()
        output_serializer = WriterSerializerWithMedia(writer,many=many)
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
    queryset = WriterMedia.objects.all()
    serializer_class = WriterCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = WriterSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        writer = serializer.save()
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
    queryset = TVShowMedia.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination
    serializer_class = TVShowSerializerWithMedia


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVShowMedia APIs'], operation_id='create independent tvshow [IsAdminOrReadOnly]',
    operation_description='create independent tvshow [IsAdminOrReadOnly]',
))
class TVShowCreateView(generics.CreateAPIView):
    queryset = TVShowMedia.objects.all()
    serializer_class = TVShowCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        tvshow = serializer.save()
        output_serializer = TVShowSerializerWithMedia(tvshow , many=many)
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
    queryset = TVShowMedia.objects.all()
    serializer_class = TVShowCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = TVShowSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        tvshow = serializer.save()
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
    queryset = SeasonMedia.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination
    serializer_class = SeasonSerializerWithMedia



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='create season for particular tvshow [IsAdminOrReadOnly]',
    operation_description='create independent tvshow [IsAdminOrReadOnly]',
))
class SeasonCreateView(generics.CreateAPIView):
    queryset = SeasonMedia.objects.all()
    serializer_class = SeasonCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        season = serializer.save()
        output_serializer = SeasonSerializerWithMedia(season , many=many)
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
    queryset = SeasonMedia.objects.all()
    serializer_class = SeasonCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = SeasonSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        season = serializer.save()
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
    queryset = EpisodeMedia.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination
    serializer_class = EpisodeSerializerWithMedia


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['📽️ App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='create episode for particular season [IsAdminOrReadOnly]',
    operation_description='create episode for particular season [IsAdminOrReadOnly]',
))
class EpisodeCreateView(generics.CreateAPIView):
    queryset = EpisodeMedia.objects.all()
    serializer_class = EpisodeCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        episode = serializer.save()
        output_serializer = EpisodeSerializerWithMedia(episode , many=many)
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
    queryset = EpisodeMedia.objects.all()
    serializer_class = EpisodeCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        output_serializer = EpisodeSerializerWithMedia(instance)
        return Response(output_serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        episode = serializer.save()
        output_serializer = EpisodeSerializerWithMedia(episode)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------------------------------------------------

