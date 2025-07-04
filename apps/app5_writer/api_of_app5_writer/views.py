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

#pagination 
from rest_framework import pagination
from shared.pagination import GlobalPagination


#permissions
from rest_framework import permissions
from shared.permissions import IsAdminOrReadOnly


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App5 : Writer APIs'], operation_id='list all  writer [IsAdminOrReadOnly] [paginate-10]',
    operation_description='list all writer [IsAdminOrReadOnly]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App5 : Writer APIs'], operation_id='create a writer [IsAdminOrReadOnly]',
    operation_description='create a writer [IsAdminOrReadOnly]',
)) 
class Writer_ListCreate_View(generics.ListCreateAPIView):
    queryset = Writer.objects.all().select_related('writermedia').prefetch_related('writermedia__media_files')
    serializer_class = WriterSerializer 
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App5 : Writer APIs'], operation_id='retrieve particular writer detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App5 : Writer APIs'], operation_id='update particular writer detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App5 : Writer APIs'], operation_id='patch particular writer detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App5 : Writer APIs'], operation_id='delete particular writer detail [IsAdminOrReadOnly]',
))
class Writer_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Writer.objects.all().select_related('writermedia').prefetch_related('writermedia__media_files')
    serializer_class = WriterSerializer 
    permission_classes = [IsAdminOrReadOnly]
 




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App5 : WriterCoreDetail APIs'], operation_id='list all  writer core detail [IsAdminOrReadOnly] [paginate-10]',
    operation_description='list all writer core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App5 : WriterCoreDetail APIs'], operation_id='create a writer core detail [IsAdminOrReadOnly]',
    operation_description='create a writer core detail [IsAdminOrReadOnly]',
)) 
class WriterCoreDetail_ListCreate_View(generics.ListCreateAPIView):
    queryset = WriterCoreDetail.objects.select_related('writer')
    serializer_class = WriterCoreDetailSerializer 
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App5 : WriterCoreDetail APIs'], operation_id='retrieve particular writer core detail detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App5 : WriterCoreDetail APIs'], operation_id='update particular writer core derial detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App5 : WriterCoreDetail APIs'], operation_id='patch particular writer core detail detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App5 : WriterCoreDetail APIs'], operation_id='delete particular writer core detail detail [IsAdminOrReadOnly]',
))
class WriterCoreDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = WriterCoreDetail.objects.all().select_related('writer')
    serializer_class = WriterCoreDetailSerializer
    permission_classes = [IsAdminOrReadOnly]


