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

class MediaFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer



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
    tags=['App1 : MovieMedia APIs'], operation_id='get all movie with media',
    operation_description='get all movie with media',
))
class MovieListView(generics.ListAPIView):
    queryset = MovieMedia.objects.all()
    serializer_class = MovieSerializerWithMedia


# For creating single movie entry
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App1 : MovieMedia APIs'], operation_id='create single movie with media',
    operation_description='create single movie with media',
))
class MovieCreateView(generics.CreateAPIView):
    queryset = MovieMedia.objects.all()
    serializer_class = MovieCreateSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data,  many=many)
        serializer.is_valid(raise_exception=True)
        movie = serializer.save()

        output_serializer = MovieSerializerWithMedia(movie, many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App1 : MovieMedia APIs'], operation_id='retrieve particular movie detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App1 : MovieMedia APIs'], operation_id='update particular movie detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App1 : MovieMedia APIs'], operation_id='patch particular movie detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App1 : MovieMedia APIs'], operation_id='delete particular movie detail',
))
class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieMedia.objects.all()
    serializer_class = MovieCreateSerializer
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
    tags=['App1 : CastMedia APIs'], operation_id='list all cast with media',
    operation_description='list all cast with media',
))
class CastListView(generics.ListAPIView):
    queryset = CastMedia.objects.all()
    serializer_class = CastSerializerWithMedia



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App1 : CastMedia APIs'], operation_id='create independent cast with media',
    operation_description='create independent cast with media',
))
class CastCreateView(generics.CreateAPIView):
    queryset = CastMedia.objects.all()
    serializer_class = CastCreateSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        cast = serializer.save()

        output_serializer = CastSerializerWithMedia(cast, many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App1 : CastMedia APIs'], operation_id='retrieve particular caste detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App1 : CastMedia APIs'], operation_id='update particular caste detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App1 : CastMedia APIs'], operation_id='patch particular caste detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App1 : CastMedia APIs'], operation_id='delete particular caste detail',
))
class CastDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CastMedia.objects.all()
    serializer_class = CastCreateSerializer
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
    tags=['App1 : CreatorMedia APIs'], operation_id='list all creator with media',
    operation_description='list all creator with media',
))
class CreatorListView(generics.ListAPIView):
    queryset = CreatorMedia.objects.all()
    serializer_class = CreatorSerializerWithMedia



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App1 : CreatorMedia APIs'], operation_id='create independent creator',
    operation_description='create independent creator',
))
class CreatorCreateView(generics.CreateAPIView):
    queryset = CreatorMedia.objects.all()
    serializer_class = CreatorCreateSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        creator = serializer.save()
        output_serializer = CreatorSerializerWithMedia(creator,many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App1 : CreatorMedia APIs'], operation_id='retrieve particular creator detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App1 : CreatorMedia APIs'], operation_id='update particular creator detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App1 : CreatorMedia APIs'], operation_id='patch particular creator detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App1 : CreatorMedia APIs'], operation_id='delete particular creator detail',
))
class CreatorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreatorMedia.objects.all()
    serializer_class = CreatorCreateSerializer
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
    tags=['App1 : WriterMedia APIs'], operation_id='list all writer with media',
    operation_description='list all writer with media',
))
class WriterListView(generics.ListAPIView):
    queryset = WriterMedia.objects.all()
    serializer_class = WriterSerializerWithMedia




@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App1 : WriterMedia APIs'], operation_id='create independent writer',
    operation_description='create independent writer',
))
class WriterCreateView(generics.CreateAPIView):
    queryset = WriterMedia.objects.all()
    serializer_class = WriterCreateSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        writer = serializer.save()
        output_serializer = WriterSerializerWithMedia(writer,many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App1 : WriterMedia APIs'], operation_id='retrieve particular writer detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App1 : WriterMedia APIs'], operation_id='update particular writer detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App1 : WriterMedia APIs'], operation_id='patch particular writer detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App1 : WriterMedia APIs'], operation_id='delete particular writer detail',
))
class WriterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WriterMedia.objects.all()
    serializer_class = WriterCreateSerializer
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
    tags=['App1 : TVShowMedia APIs'], operation_id='list all tvshow with media',
    operation_description='list all tvshow with media',
))
class TvShowListView(generics.ListAPIView):
    queryset = TVShowMedia.objects.all()
    serializer_class = TVShowSerializerWithMedia


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App1 : TVShowMedia APIs'], operation_id='create independent tvshow',
    operation_description='create independent tvshow',
))
class TVShowCreateView(generics.CreateAPIView):
    queryset = TVShowMedia.objects.all()
    serializer_class = TVShowCreateSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        tvshow = serializer.save()
        output_serializer = TVShowSerializerWithMedia(tvshow , many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App1 : TVShowMedia APIs'], operation_id='retrieve particular tvshow detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App1 : TVShowMedia APIs'], operation_id='update particular tvshow detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App1 : TVShowMedia APIs'], operation_id='patch particular tvshow detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App1 : TVShowMedia APIs'], operation_id='delete particular tvshow detail',
))
class TVShowDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TVShowMedia.objects.all()
    serializer_class = TVShowCreateSerializer
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
    tags=['App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='list all season for particular tvshow',
    operation_description='list all season for particular tvshow',
))
class SeasonListView(generics.ListAPIView):
    queryset = SeasonMedia.objects.all()
    serializer_class = SeasonSerializerWithMedia



@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='create season for particular tvshow',
    operation_description='create independent tvshow',
))
class SeasonCreateView(generics.CreateAPIView):
    queryset = SeasonMedia.objects.all()
    serializer_class = SeasonCreateSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        season = serializer.save()
        output_serializer = SeasonSerializerWithMedia(season , many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='retrieve particular season detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='update particular season detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='patch particular season detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App1 : TVshowMedia -> SeasonMedia  APIs'], operation_id='delete particular season detail',
))
class SeasonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SeasonMedia.objects.all()
    serializer_class = SeasonCreateSerializer
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
    tags=['App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='list all episode with media',
    operation_description='list all episode with media',
))
class EpisodeListView(generics.ListAPIView):
    queryset = EpisodeMedia.objects.all()
    serializer_class = EpisodeSerializerWithMedia


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='create episode for particular season',
    operation_description='create independent tvshow',
))
class EpisodeCreateView(generics.CreateAPIView):
    queryset = EpisodeMedia.objects.all()
    serializer_class = EpisodeCreateSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        episode = serializer.save()
        output_serializer = EpisodeSerializerWithMedia(episode , many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='retrieve particular episode detail',
)) 
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='update particular episode detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='patch particular episode detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App1 : TVshowMedia -> SeasonMedia -> EpisodeMedia APIs'], operation_id='delete particular episode detail',
))
class EpisodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EpisodeMedia.objects.all()
    serializer_class = EpisodeCreateSerializer
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

