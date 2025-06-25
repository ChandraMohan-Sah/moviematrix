# views.py
from app5_writer.models import Writer, WriterCoreDetail
from .serializers import (
    WriterSerializer,
    WriterCoreDetailSerializer
)
from rest_framework import generics 


# swagger docs 
from drf_yasg.utils import swagger_auto_schema 
from django.utils.decorators import method_decorator 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App5 : Writer APIs'], operation_id='list all  writer',
    operation_description='list all writer',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App5 : Writer APIs'], operation_id='create a writer',
    operation_description='create a writer',
)) 
class Writer_ListCreate_View(generics.ListCreateAPIView):
    queryset = Writer.objects.all().select_related('writermedia').prefetch_related('writermedia__media_files')
    serializer_class = WriterSerializer 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App5 : Writer APIs'], operation_id='retrieve particular writer detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App5 : Writer APIs'], operation_id='update particular writer detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App5 : Writer APIs'], operation_id='patch particular writer detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App5 : Writer APIs'], operation_id='delete particular writer detail',
))
class Writer_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Writer.objects.all().select_related('writermedia').prefetch_related('writermedia__media_files')
    serializer_class = WriterSerializer 





@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App5 : WriterCoreDetail APIs'], operation_id='list all  writer core detail',
    operation_description='list all writer core detail',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App5 : WriteCoreDetail APIs'], operation_id='create a writer core detail',
    operation_description='create a writer core detail',
)) 
class WriterCoreDetail_ListCreate_View(generics.ListCreateAPIView):
    queryset = WriterCoreDetail.objects.select_related('writer')
    serializer_class = WriterCoreDetailSerializer 



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App5 : WriterCoreDetail APIs'], operation_id='retrieve particular writer core detail detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App5 : WriterCoreDetail APIs'], operation_id='update particular writer core derial detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App5 : WriterCoreDetail APIs'], operation_id='patch particular writer core detail detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App5 : WriterCoreDetail APIs'], operation_id='delete particular writer core detail detail',
))
class WriterCoreDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = WriterCoreDetail.objects.all().select_related('writer')
    serializer_class = WriterCoreDetailSerializer


