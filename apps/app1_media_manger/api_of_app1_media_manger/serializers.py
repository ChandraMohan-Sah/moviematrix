# serializers.py
from rest_framework import serializers 
from app1_media_manger.models import (
    CastMedia,  CreatorMedia, WriterMedia, MovieMedia,
    EpisodeMedia, SeasonMedia,  TVShowMedia,  MediaFile
)

from django.contrib.contenttypes.models import ContentType


'''
✅  When should you use two serializers?
    : Use two serializers when:
        - Your input fields ≠ model fields (custom logic, nested creation).
        - Your output needs extra/related data (like media_files, IDs, etc.).
        - You want to keep logic clean and separated.
'''

# media file serializer 
# -------------------------------------------------------------------------------------------
class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile 
        fields = ['id', 'media_type', 'file', 'cdn_url', 'uploaded_at']



# Mixin to Fetch Media from GenericRelation
# -------------------------------------------------------------------------------------------
class MediaFileMixin:
    def get_media(self, obj, media_type):
        return MediaFileSerializer(obj.media_files.filter(media_type=media_type), many=True).data



# GET only : With Media Serializers - All Simplified Using GenericRelation 
# -------------------------------------------------------------------------------------------
class CastSerializerWithMedia(serializers.ModelSerializer, MediaFileMixin):
    profile_pics = serializers.SerializerMethodField()
    related_pics = serializers.SerializerMethodField()

    class Meta:
        model = CastMedia 
        fields = ['id', 'name', 'profile_pics', 'related_pics']

    def get_profile_pics(self, obj):
        return self.get_media(obj, 'profile_pic')

    def get_related_pics(self, obj):
        return self.get_media(obj, 'related_pic')


class CreatorSerializerWithMedia(serializers.ModelSerializer, MediaFileMixin):
    profile_pics = serializers.SerializerMethodField()
    related_pics = serializers.SerializerMethodField()

    class Meta:
        model = CreatorMedia
        fields = ['id', 'name', 'profile_pics', 'related_pics']

    def get_profile_pics(self, obj):
        return self.get_media(obj, 'profile_pic')

    def get_related_pics(self, obj):
        return self.get_media(obj, 'related_pic')


class WriterSerializerWithMedia(serializers.ModelSerializer, MediaFileMixin):
    profile_pics = serializers.SerializerMethodField()
    related_pics = serializers.SerializerMethodField() 

    class Meta:
        model = WriterMedia
        fields =  ['id', 'name', 'profile_pics', 'related_pics']

    def get_profile_pics(self,obj):
        return self.get_media(obj, 'profile_pic')
    
    def get_related_pics(self, obj):
        return self.get_media(obj,'related_pic')
    

class MovieSerializerWithMedia(serializers.ModelSerializer, MediaFileMixin):
    banners = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()
    trailers = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    related_pics = serializers.SerializerMethodField()

    class Meta:
        model = MovieMedia
        fields = ['id', 'name', 'banners', 'thumbnails', 'trailers', 'videos', 'related_pics']

    def get_banners(self, obj):
        return self.get_media(obj, 'banner')

    def get_thumbnails(self, obj):
        return self.get_media(obj, 'thumbnail')

    def get_trailers(self, obj):
        return self.get_media(obj, 'trailer')

    def get_videos(self, obj):
        return self.get_media(obj, 'video')

    def get_related_pics(self, obj):
        return self.get_media(obj, 'related_pic')
    

class EpisodeSerializerWithMedia(serializers.ModelSerializer, MediaFileMixin):
    thumbnails = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()

    class Meta:
        model = EpisodeMedia
        fields = ['id', 'title', 'tvshow', 'season', 'thumbnails', 'videos']

    def get_thumbnails(self, obj):
        return self.get_media(obj, 'thumbnail')

    def get_videos(self, obj):
        return self.get_media(obj, 'video')



class SeasonSerializerWithMedia(serializers.ModelSerializer):
    tvshow = serializers.SlugRelatedField(slug_field='name', queryset=TVShowMedia.objects.all())
    episodes = EpisodeSerializerWithMedia(many=True, read_only=True)

    class Meta:
        model = SeasonMedia
        fields = ['id', 'season_number', 'tvshow', 'episodes']




class TVShowSerializerWithMedia(serializers.ModelSerializer, MediaFileMixin):
    seasons = SeasonSerializerWithMedia(many=True, read_only=True)
    banners = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()
    trailers = serializers.SerializerMethodField()

    class Meta:
        model = TVShowMedia
        fields = ['id', 'name', 'seasons', 'banners', 'thumbnails', 'trailers']

    def get_banners(self, obj):
        return self.get_media(obj, 'banner')

    def get_thumbnails(self, obj):
        return self.get_media(obj, 'thumbnail')

    def get_trailers(self, obj):
        return self.get_media(obj, 'trailer')



# Create Serializers — Just for POSTing URLs
# -----------------------------------------------------------------------------------------
class MovieCreateSerializer(serializers.ModelSerializer):
    banners = serializers.ListField(child=serializers.URLField(), required=False)
    thumbnails = serializers.ListField(child=serializers.URLField(), required=False)
    trailers = serializers.ListField(child=serializers.URLField(), required=False)
    videos = serializers.ListField(child=serializers.URLField(), required=False)
    related_pics = serializers.ListField(child=serializers.URLField(), required=False)

    class Meta:
        model = MovieMedia
        fields = ['name', 'banners', 'thumbnails', 'trailers', 'videos', 'related_pics']

    def create(self, validated_data):
        banners = validated_data.pop('banners', [])
        thumbnails = validated_data.pop('thumbnails', [])
        trailers = validated_data.pop('trailers', [])
        videos = validated_data.pop('videos', [])
        related_pics = validated_data.pop('related_pics', [])

        movie = MovieMedia.objects.create(**validated_data)
        content_type = ContentType.objects.get_for_model(movie)

        def create_media_files(urls, media_type):
            for url in urls:
                MediaFile.objects.create(
                    content_type=content_type,
                    object_id=movie.id,
                    cdn_url=url,
                    media_type=media_type
                )

        create_media_files(banners, 'banner')
        create_media_files(thumbnails, 'thumbnail')
        create_media_files(trailers, 'trailer')
        create_media_files(videos, 'video')
        create_media_files(related_pics, 'related_pic')

        return movie




class CastCreateSerializer(serializers.ModelSerializer):
    profile_pics = serializers.ListField(child=serializers.URLField(), required=False)
    related_pics = serializers.ListField(child=serializers.URLField(), required=False)

    class Meta:
        model = CastMedia
        fields = ['name', 'profile_pics', 'related_pics']

    def create(self, validated_data):
        profile_pics = validated_data.pop('profile_pics', [])
        related_pics = validated_data.pop('related_pics', [])

        cast = CastMedia.objects.create(**validated_data)
        content_type = ContentType.objects.get_for_model(cast)

        def create_media_files(urls, media_type):
            for url in urls:
                MediaFile.objects.create(
                    content_type=content_type,
                    object_id=cast.id,
                    cdn_url=url,
                    media_type=media_type
                )

        create_media_files(profile_pics, 'profile_pic')
        create_media_files(related_pics, 'related_pic')

        return cast


class CreatorCreateSerializer(serializers.ModelSerializer):
    profile_pics = serializers.ListField(child=serializers.URLField(), required=False)
    related_pics = serializers.ListField(child=serializers.URLField(), required=False)

    class Meta:
        model = CreatorMedia
        fields = ['name', 'profile_pics', 'related_pics']

    def create(self, validated_data):
        profile_pics = validated_data.pop('profile_pics', [])
        related_pics = validated_data.pop('related_pics', [])

        creator = CreatorMedia.objects.create(**validated_data)
        content_type = ContentType.objects.get_for_model(creator)

        def create_media_files(urls, media_type):
            for url in urls:
                MediaFile.objects.create(
                    content_type=content_type,
                    object_id=creator.id,
                    cdn_url=url,
                    media_type=media_type
                )

        create_media_files(profile_pics, 'profile_pic')
        create_media_files(related_pics, 'related_pic')

        return creator





class WriterCreateSerializer(serializers.ModelSerializer):
    profile_pics = serializers.ListField(child=serializers.URLField(), required=False)
    related_pics = serializers.ListField(child = serializers.URLField(), required= False)

    class Meta:
        model = WriterMedia 
        fields = ['name', 'profile_pics', 'related_pics'] 
    
    def create(self, validated_data):
        profile_pics = validated_data.pop('profile_pics', [])
        related_pics = validated_data.pop('related_pics', [])

        writer = WriterMedia.objects.create(**validated_data)
        content_type = ContentType.objects.get_for_model(writer)

        def create_media_files(urls, media_type):
            for url in urls:
                MediaFile.objects.create(
                    content_type=content_type,
                    object_id=writer.id,
                    cdn_url=url,
                    media_type=media_type
                )

        create_media_files(profile_pics, 'profile_pic')
        create_media_files(related_pics, 'related_pic')

        return writer  




class TVShowCreateSerializer(serializers.ModelSerializer):
    banners = serializers.ListField(child=serializers.URLField(), required=False)
    thumbnails = serializers.ListField(child=serializers.URLField(), required=False)
    trailers = serializers.ListField(child=serializers.URLField(), required=False)
    videos = serializers.ListField(child=serializers.URLField(), required=False)
    related_pics = serializers.ListField(child=serializers.URLField(), required=False)

    class Meta:
        model = TVShowMedia
        fields = '__all__'

    def create(self, validated_data):
        banners = validated_data.pop('banners', [])
        thumbnails = validated_data.pop('thumbnails', [])
        trailers = validated_data.pop('trailers', [])
        videos = validated_data.pop('videos', [])
        related_pics = validated_data.pop('related_pics', [])

        tvshow = TVShowMedia.objects.create(**validated_data)

        content_type = ContentType.objects.get_for_model(tvshow)

        # Helper function to create MediaFile objects for a list of URLs with a media_type
        def create_media_files(urls, media_type):
            for url in urls:
                MediaFile.objects.create(
                    content_type=content_type,
                    object_id=tvshow.id,
                    cdn_url=url,
                    media_type=media_type
                )

        create_media_files(banners, 'banner')
        create_media_files(thumbnails, 'thumbnail')
        create_media_files(trailers, 'trailer')
        create_media_files(videos, 'video')
        create_media_files(related_pics, 'related_pic')

        return tvshow



class SeasonCreateSerializer(serializers.ModelSerializer):
    banners = serializers.ListField(child=serializers.URLField(), required=False)
    thumbnails = serializers.ListField(child=serializers.URLField(), required=False)

    class Meta:
        model = SeasonMedia
        fields = ['tvshow', 'season_number', 'banners', 'thumbnails']  # be explicit

    def create(self, validated_data):
        banners = validated_data.pop('banners', [])
        thumbnails = validated_data.pop('thumbnails', [])

        season = SeasonMedia.objects.create(**validated_data)
        content_type = ContentType.objects.get_for_model(season)

        def create_media_files(urls, media_type):
            for url in urls:
                MediaFile.objects.create(
                    content_type=content_type,
                    object_id=season.id,
                    cdn_url=url,
                    media_type=media_type
                )

        create_media_files(banners, 'banner')
        create_media_files(thumbnails, 'thumbnail')
        return season



class EpisodeCreateSerializer(serializers.ModelSerializer):
    thumbnails = serializers.ListField(child=serializers.URLField(), required=False)

    class Meta:
        model = EpisodeMedia
        fields = '__all__'

    def create(self, validated_data):
        thumbnails = validated_data.pop('thumbnails', [])

        episode = EpisodeMedia.objects.create(**validated_data)
        content_type = ContentType.objects.get_for_model(episode)

        def create_media_files(urls, media_type):
            for url in urls:
                MediaFile.objects.create(
                    content_type=content_type,
                    object_id=episode.id,
                    cdn_url=url,
                    media_type=media_type
                )

        create_media_files(thumbnails, 'thumbnail')
        return episode
    
# -------------------------------------------------------------------------------------------