# # serializers.py
# from rest_framework import serializers 
# from app9_season.models import Season 
# from app1_media_manger.models import SeasonMedia


# class SeasonSerializer(serializers.ModelSerializer): 
#     title = serializers.CharField(source='seasonmedia.tvshow.name', read_only=True)
#     season_number = serializers.IntegerField(source='seasonmedia.season_number', read_only=True)

#     seasonmedia = serializers.PrimaryKeyRelatedField(
#         queryset=SeasonMedia.objects.all()
#     )


#     class Meta: 
#         model = Season
#         fields = [
#             'id',
#             'seasonmedia',
#             'title',
#             'season_number'
#         ]
#         ref_name = "App9-SeasonSerializer"  


