from app3_cast.models import Cast, CastCoreDetail
from .serializers import (
    CastSerializer,
    CastCoreDetailSerializer
)
from rest_framework import generics

from app1_media_manger.api_of_app1_media_manger.serializers import MediaFile
from app3_cast.models import CastMedia
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch

#swagger docs
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

#pagination 
from rest_framework import pagination
from shared.pagination import GlobalPagination


#permissions
from rest_framework import permissions
from shared.permissions import IsAdminOrReadOnly

@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App3 : Cast APIs'], operation_id='list all  cast [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all cast',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App3 : Cast APIs'], operation_id='create a cast [IsAdminOrReadOnly]',
    operation_description='create a cast',
))
class Cast_ListCreate_View(generics.ListCreateAPIView):
    queryset = Cast.objects.select_related('castmedia').prefetch_related('castmedia__media_files').all()
    serializer_class = CastSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination


 
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App3 : Cast APIs'], operation_id='retrieve particular cast detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App3 : Cast APIs'], operation_id='update particular cast detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App3 : Cast APIs'], operation_id='patch particular cast detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App3 : Cast APIs'], operation_id='delete particular cast detail [IsAdminOrReadOnly]',
))
class Cast_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cast.objects.select_related('cast').prefetch_related('castmedia__media_files')
    serializer_class = CastSerializer
    permission_classes = [IsAdminOrReadOnly]




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App3 : CastCoreDetail APIs'], operation_id='list all core detail of  cast [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all core detail of  cast [IsAdminOrReadOnly]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App3 : CastCoreDetail APIs'], operation_id='create a core detail of cast [IsAdminOrReadOnly]',
    operation_description='create a core detail of cast [IsAdminOrReadOnly]',
))
class CastCoreDetail_ListCreate_View(generics.ListCreateAPIView):
    queryset = CastCoreDetail.objects.select_related('cast')
    serializer_class = CastCoreDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App3 : CastCoreDetail APIs'], operation_id='retrieve particular cast core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App3 : CastCoreDetail APIs'], operation_id='update particular cast core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App3 : CastCoreDetail APIs'], operation_id='patch particular cast core detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App3 : CastCoreDetail APIs'], operation_id='delete particular cast core detail [IsAdminOrReadOnly]',
))
class CastCoreDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = CastCoreDetail.objects.select_related('cast__castmedia').prefetch_related('cast__castmedia__media_files')
    serializer_class = CastCoreDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
 