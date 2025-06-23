# serializers.py
from rest_framework import serializers 
from django.contrib.contenttypes.models import ContentType

from app1_media_manger.models import MediaFile, CreatorMedia
from app4_creator.models import Creator, CreatorCoreDetail



class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['id', 'media_type', 'file', 'cdn_url', 'uploaded_at']
        ref_name="app4-mediafileserializer"




class CreatorSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creatormedia.name', read_only=True)
    profile_pic = MediaFileSerializer(many=True, read_only=True)
    related_pic = MediaFileSerializer(many=True, read_only=True)

    creatormedia = serializers.SlugRelatedField(
        slug_field='name',              # Match using `name` instead of ID
        queryset=CreatorMedia.objects.all()
    )  


    class Meta:
        model = Creator
        fields = [
            'id',
            'creatormedia',         # for creation (write-only)
            'creator_name',      # read-only : comes from app1 CreatorMedia model
            'profile_pic',
            'related_pic',
            'creator_created',
            'creator_updated',
        ]



class CreatorCoreDetailSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)
    creator_id = serializers.PrimaryKeyRelatedField(
        queryset=Creator.objects.all(),
        source='creator',
        write_only=True 
    )

    # spouses, children, relatives, otherwork are JSONFields so DRF handles them natively as lists
    spouses = serializers.ListField(child=serializers.CharField(), required=False)
    children = serializers.ListField(child=serializers.CharField(), required=False)
    relatives = serializers.ListField(child=serializers.CharField(), required=False)
    otherwork = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta: 
        model = CreatorCoreDetail
        fields = [
            'id',
            'creator',
            'creator_id',
            'height',
            'born_date',
            'death_date',
            'spouses',
            'children',
            'relatives',
            'otherwork',
        ]
