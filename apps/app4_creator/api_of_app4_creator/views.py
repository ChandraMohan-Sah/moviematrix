# views.py
from app4_creator.models import Creator, CreatorCoreDetail
from .serializers import (
    CreatorSerializer, 
    CreatorCoreDetailSerializer
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
    tags=['App4 : Creator APIs'], operation_id='list all  creator [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all creator [IsAdminOrReadOnly]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App4 : Creator APIs'], operation_id='create a creator [IsAdminOrReadOnly]',
    operation_description='create a creator [IsAdminOrReadOnly]',
)) 
class Creator_ListCreate_View(generics.ListCreateAPIView):
    queryset = Creator.objects.all().select_related('creatormedia').prefetch_related('creatormedia__media_files')
    serializer_class = CreatorSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination

 

@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App4 : Creator APIs'], operation_id='retrieve particular creator detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App4 : Creator APIs'], operation_id='update particular creator detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App4 : Creator APIs'], operation_id='patch particular creator detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App4 : Creator APIs'], operation_id='delete particular creator detail [IsAdminOrReadOnly]',
))
class Creator_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Creator.objects.all().select_related('creatormedia').prefetch_related('creatormedia__media_files')
    serializer_class = CreatorSerializer
    permission_classes = [IsAdminOrReadOnly]


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App4 : CreatorCoreDetail APIs'], operation_id='list all core detail of  creator [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all core detail of  creator [IsAdminOrReadOnly]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App4 : CreatorCoreDetail APIs'], operation_id='create a core detail of creator [IsAdminOrReadOnly]',
    operation_description='create a core detail of creator [IsAdminOrReadOnly]',
))
class CreatorCoreDetail_ListCreate_View(generics.ListCreateAPIView):
    queryset = CreatorCoreDetail.objects.select_related('creator')
    serializer_class = CreatorCoreDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App4 : CreatorCoreDetail APIs'], operation_id='retrieve particular creator core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App4 : CreatorCoreDetail APIs'], operation_id='update particular creator core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App4 : CreatorCoreDetail APIs'], operation_id='patch particular creator core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App4 : CreatorCoreDetail APIs'], operation_id='delete particular creator core detail [IsAdminOrReadOnly]',
))
class CreatorCoreDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreatorCoreDetail.objects.select_related('creator')
    serializer_class = CreatorCoreDetailSerializer
    permission_classes = [IsAdminOrReadOnly]



# @method_decorator(name='get', decorator=swagger_auto_schema(
#     tags=['App5 : Writer APIs'], operation_id='list all  writer',
#     operation_description='list all writer',
# ))
# @method_decorator(name='post', decorator=swagger_auto_schema(
#     tags=['App5 : Writer APIs'], operation_id='create a writer',
#     operation_description='create a writer',
# )) 


# @method_decorator(name='get', decorator=swagger_auto_schema(
#     tags=['App5 : WriterCoreDetail APIs'], operation_id='retrieve particular writer detail',
# ))
# @method_decorator(name='put', decorator=swagger_auto_schema(
#     tags=['App5 : WriterCoreDetail APIs'], operation_id='update particular writer detail',
# ))
# @method_decorator(name='patch', decorator=swagger_auto_schema(
#     tags=['App5 : WriterCoreDetail APIs'], operation_id='patch particular writer detail',
# ))
# @method_decorator(name='delete', decorator=swagger_auto_schema(
#     tags=['App5 : WriterCoreDetail APIs'], operation_id='delete particular writer detail',
# ))