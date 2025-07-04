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



class CastSerializer(serializers.ModelSerializer):
    cast_name = serializers.CharField(source='castmedia.name', read_only=True)
    profile_pic = MediaFileSerializer(many=True, read_only=True)
    related_pic = MediaFileSerializer(many=True, read_only=True)

    # Accept castmedia ID when creating
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



class CastCoreDetailSerializer(serializers.ModelSerializer):
    cast = CastSerializer(read_only=True)
    cast_id = serializers.PrimaryKeyRelatedField(
        queryset=Cast.objects.all(), source='cast', write_only=True
    )

    # spouses, children, relatives, otherwork are JSONFields so DRF handles them natively as lists
    spouses = serializers.ListField(child=serializers.CharField(), required=False)
    children = serializers.ListField(child=serializers.CharField(), required=False)
    relatives = serializers.ListField(child=serializers.CharField(), required=False)
    otherwork = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = CastCoreDetail
        fields = [
            'id',
            'cast',
            'cast_id',
            'height',
            'born_date',
            'death_date',
            'spouses',
            'children',
            'relatives',
            'otherwork',
        ]
