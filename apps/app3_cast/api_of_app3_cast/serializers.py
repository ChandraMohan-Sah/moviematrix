# serializers.py
from rest_framework import serializers 
from app1_media_manger.models  import MediaFile
from app3_cast.models import Cast, CastCoreDetail, CastKnownFor
from django.contrib.contenttypes.models import ContentType

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile 
        fields = ['id', 'media_type', 'cdn_url', 'uploaded_at']


class CastSerializer(serializers.ModelSerializer):
    cast_name = serializers.ReadOnlyField()
    profile_pic = MediaFileSerializer(many=True, read_only=True)
    related_pic = MediaFileSerializer(many=True, read_only=True)

    class Meta:
        model = Cast
        fields = ['id', 'cast_name', 'profile_pic', 'related_pic', 'cast_created', 'cast_updated']



class CastCoreDetailSerializer(serializers.ModelSerializer):
    cast = serializers.PrimaryKeyRelatedField(queryset=Cast.objects.all())
    spouses = serializers.PrimaryKeyRelatedField(queryset=Cast.objects.all(), many=True, required=False)
    children = serializers.PrimaryKeyRelatedField(queryset=Cast.objects.all(), many=True, required=False)
    relatives = serializers.PrimaryKeyRelatedField(queryset=Cast.objects.all(), many=True, required=False)

    class Meta: 
        model = CastCoreDetail 
        fields = [
            'id', 'cast', 'height', 'born_date', 'death_date',
            'spouses', 'children', 'relatives', 'otherwork'
        ]


class CastKnownForSerializer(serializers.ModelSerializer):
    cast = serializers.PrimaryKeyRelatedField(queryset=Cast.objects.all())
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.filter(model__in=['moviemedia', 'tvshowmedia'])
    )

    object_id = serializers.IntegerField()
    known_work_display = serializers.SerializerMethodField() 

    class Meta:
        model = CastKnownFor
        fields = ['id', 'cast', 'content_type', 'object_id', 'known_work_display']

    def get_known_work_display(self, obj):
        return str(obj.known_work)