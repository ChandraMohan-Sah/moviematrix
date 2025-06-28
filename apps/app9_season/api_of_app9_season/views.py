# # views.py
# from rest_framework import generics 
# from app9_season.models import Season 
# from .serializers import SeasonSerializer



# # swagger docs 
# from drf_yasg.utils import swagger_auto_schema 
# from django.utils.decorators import method_decorator 


# @method_decorator(name='get', decorator=swagger_auto_schema(
#     tags=['App9 : Season APIs'], operation_id='list all season available',
#     operation_description='list all season available',
# ))
# @method_decorator(name='post', decorator=swagger_auto_schema(
#     tags=['App9 : Season APIs'], operation_id='create a season',
#     operation_description='create a season',
# )) 
# class Season_LC_View(generics.ListCreateAPIView):
#     queryset = Season.objects.all().select_related('seasonmedia').prefetch_related('seasonmedia__media_files')
#     serializer_class = SeasonSerializer




# @method_decorator(name='get', decorator=swagger_auto_schema(
#     tags=['App9 : Season APIs'], operation_id='retrieve particular season detail',
# ))
# @method_decorator(name='put', decorator=swagger_auto_schema(
#     tags=['App9 : Season APIs'], operation_id='update particular seaon detail',
# ))
# @method_decorator(name='patch', decorator=swagger_auto_schema(
#     tags=['App9 : Season APIs'], operation_id='patch particular season detail',
# ))
# @method_decorator(name='delete', decorator=swagger_auto_schema(
#     tags=['App9 : Season APIs'], operation_id='delete particular season detail',
# ))
# class Season_RUD_View(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Season.objects.all().select_related('seasonmedia').prefetch_related('seasonmedia__media_files')
#     serializer_class = SeasonSerializer

 