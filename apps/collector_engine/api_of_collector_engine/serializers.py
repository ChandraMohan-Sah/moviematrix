# serializers.py
from rest_framework import serializers 
from app6_movie.models import Movie
from app1_media_manger.models import MediaFile
from app3_cast.models import Cast


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MediaFile 
        fields = ['id', 'media_type', 'file', 'cdn_url', 'uploaded_at']
        ref_name = "app6-mediafilemanager"


class MediaFileMixin:
    def get_media(self, obj, media_type):
        media_list = list(obj.media_files.all()) # 'media_files' must be prefetched on the queryset to avoid extra DB queries
        
        filtered_media = []
        for m in media_list:
            if m.media_type == media_type:
                filtered_media.append(m)

        return MediaFileSerializer(filtered_media, many=True).data



class LightMovieSerializer(serializers.ModelSerializer, MediaFileMixin):
    movie_name = serializers.CharField(source='moviemedia.name', read_only=True)
    thumbnails = serializers.SerializerMethodField()
    avg_rating = serializers.FloatField(source='movie_general_detail.avg_rating', read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'movie_name',
            'thumbnails',
            'avg_rating',
        ]
    
    def get_thumbnails(self, obj):
        return self.get_media(obj.moviemedia, 'thumbnail')


class PopularCastSerializer(serializers.ModelSerializer, MediaFileMixin):
    cast_name = serializers.CharField(source='castmedia.name', read_only=True)
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Cast 
        fields = [
            'id',
            'cast_name',
            'profile_pic'
        ]
    
    def get_profile_pic(self, obj):
        return self.get_media(obj.castmedia, 'profile_pic')
    

class IMDBOriginalsSerializer(serializers.ModelSerializer, MediaFileMixin):
    movie_name = serializers.CharField(source='moviemedia.name', read_only=True)
    thumbnails = serializers.SerializerMethodField()
    trailers = serializers.SerializerMethodField()
    duration = serializers.FloatField(source='movie_general_detail.duration', read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'movie_name',
            'trailers',
            'thumbnails',
            'duration',
        ]
    
    def get_trailers(self, obj):
        return self.get_media(obj.moviemedia, 'trailer')


    def get_thumbnails(self, obj):
        return self.get_media(obj.moviemedia, 'thumbnail')