# serializers.py
from rest_framework import serializers 
from django.contrib.contenttypes.models import ContentType

from app1_media_manger.api_of_app1_media_manger.serializers  import CastSerializerWithMedia
from app1_media_manger.models import MediaFile, CastMedia
from app3_cast.models import Cast, CastCoreDetail
from app3_cast.models import Cast


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['id', 'media_type', 'file', 'cdn_url', 'uploaded_at']
        ref_name="app4-mediafileserializer"


# class MediaFileMixin:
#     def get_media(self, obj, media_type):
#         media_list = obj.media_files.all()  # 'media_files' must be prefetched on the queryset to avoid extra DB queries
        
#         filtered_media = []
#         for m in media_list:
#             if m.media_type == media_type:
#                 filtered_media.append(m)

#         return MediaFileSerializer(filtered_media, many=True).data
 

# class MediaFileMixin:
#     def get_media(self, obj, media_type):
#         # Avoid triggering an extra DB query by relying on prefetched 'media_files'
#         media_list = list(getattr(obj, 'media_files', []))  # Use list instead of .all()
        
#         # Filter in memory (no DB hit)
#         filtered_media = [m for m in media_list if m.media_type == media_type]

#         return MediaFileSerializer(filtered_media, many=True).data
    
class MediaFileMixin:
    def get_media(self, obj, media_type):
        # Avoid triggering an extra DB query by relying on prefetched 'media_files'
        media_manager = getattr(obj, 'media_files', None)
        media_list = list(media_manager.all()) if media_manager else []
        
        # Filter in memory (no DB hit if prefetch_related is used)
        filtered_media = [m for m in media_list if m.media_type == media_type]

        return MediaFileSerializer(filtered_media, many=True).data
    
class CastSerializer(serializers.ModelSerializer, MediaFileMixin):
    cast_name = serializers.CharField(source='castmedia.name', read_only=True)
    profile_pic = serializers.SerializerMethodField()
    related_pic = serializers.SerializerMethodField()

    # Accept castmedia  when creating
    # castmedia = serializers.PrimaryKeyRelatedField(queryset=CastMedia.objects.all(), write_only=True)
    castmedia = serializers.SlugRelatedField(
        slug_field='name',              # Match using `name` instead of ID
        queryset=CastMedia.objects.all(),
        write_only=True
    )
 
    class Meta:
        model = Cast
        fields = [
            'id',
            'castmedia',      # for creation (write-only)
            'cast_name',      # read-only : comes from app1 CastMedia model
            'profile_pic',
            'related_pic',
            'cast_created',
            'cast_updated',
        ]
        ref_name = 'app3-castserializer'


    def get_profile_pic(self, obj):
        return self.get_media(obj.castmedia, 'profile_pic')
    
    def get_related_pic(self, obj):
        return self.get_media(obj.castmedia, 'related_pic')


class CastCoreDetailSerializer(serializers.ModelSerializer):
    cast_id = serializers.PrimaryKeyRelatedField(
        queryset=Cast.objects.select_related('castmedia').all(), write_only=True 
    )
    # cast_name = serializers.SerializerMethodField()

    # spouses, children, relatives, otherwork are JSONFields so DRF handles them natively as lists
    spouses = serializers.ListField(child=serializers.CharField(), required=False)
    children = serializers.ListField(child=serializers.CharField(), required=False)
    relatives = serializers.ListField(child=serializers.CharField(), required=False)
    otherwork = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = CastCoreDetail
        fields = [
            'id',
            'cast_id',
            # 'cast_name',
            'height',
            'born_date',  
            'death_date',
            'spouses',
            'children',
            'relatives',
            'otherwork',
        ]

    # def get_cast_name(self, obj):
    #     return obj.cast.cast_name if obj.cast else None
    


    