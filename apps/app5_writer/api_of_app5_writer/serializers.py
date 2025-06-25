# serializers.py

from rest_framework import serializers
from app1_media_manger.models import MediaFile 
from app5_writer.models import Writer, WriterMedia, WriterCoreDetail

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MediaFile 
        fields = ['id', 'media_type', 'file', 'cdn_url', 'uploaded_at']
        ref_name = "app5-mediafileserializer"


class WriterSerializer(serializers.ModelSerializer):
    writer_name = serializers.CharField(source='writermedia.name', read_only=True)
    profile_pic = MediaFileSerializer(many=True, read_only=True)
    related_pic = MediaFileSerializer(many=True, read_only=True)

    writermedia = serializers.SlugRelatedField(
        slug_field = 'name',  # Match using `name` instead of ID
        queryset=WriterMedia.objects.all()
    )

    class Meta: 
        model = Writer 
        fields = [
            'id',
            'writermedia',    # for creation (write-only)
            'writer_name',    # read-only : comes from app1 WriterMedia model
            'profile_pic',
            'related_pic',
            'writer_created',
            'writer_updated'
        ]


class WriterCoreDetailSerializer(serializers.ModelSerializer):
    writer = WriterSerializer(read_only = True)
    writer_id = serializers.PrimaryKeyRelatedField(
        queryset = Writer.objects.all(),
        source='writer',
        write_only=True
    )

    # spouses, children, relatives, otherwork are JSONFields so DRF handles them natively as lists
    spouses = serializers.ListField(child=serializers.CharField(), required=False)
    children = serializers.ListField(child=serializers.CharField(), required=False)
    relatives = serializers.ListField(child=serializers.CharField(), required=False)
    otherwork = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta: 
        model = WriterCoreDetail 
        fields = [
            'id',
            'writer',
            'writer_id',
            'height',
            'born_date',
            'death_date',
            'spouses',
            'children',
            'relatives',
            'otherwork',           
        ]