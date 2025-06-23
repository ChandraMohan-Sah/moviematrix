from app3_cast.models import Cast, CastCoreDetail
from .serializers import (
    CastSerializer,
    CastCoreDetailSerializer
)
from rest_framework import generics


#swagger docs
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App3 : Cast APIs'], operation_id='list all  cast',
    operation_description='list all cast',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App3 : Cast APIs'], operation_id='create a cast',
    operation_description='create a cast',
))
class Cast_ListCreate_View(generics.ListCreateAPIView):
    queryset = Cast.objects.all().select_related('castmedia').prefetch_related('castmedia__media_files')
    serializer_class = CastSerializer


 
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App3 : Cast APIs'], operation_id='retrieve particular cast detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App3 : Cast APIs'], operation_id='update particular cast detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App3 : Cast APIs'], operation_id='patch particular cast detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App3 : Cast APIs'], operation_id='delete particular cast detail',
))
class Cast_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cast.objects.all().select_related('castmedia').prefetch_related('castmedia__media_files')
    serializer_class = CastSerializer




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App3 : CastCoreDetail APIs'], operation_id='list all core detail of  cast',
    operation_description='list all core detail of  cast',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App3 : CastCoreDetail APIs'], operation_id='create a core detail of cast',
    operation_description='create a core detail of cast',
))
class CastCoreDetail_ListCreate_View(generics.ListCreateAPIView):
    queryset = CastCoreDetail.objects.select_related('cast')
    serializer_class = CastCoreDetailSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App3 : CastCoreDetail APIs'], operation_id='retrieve particular cast core detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App3 : CastCoreDetail APIs'], operation_id='update particular cast core detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App3 : CastCoreDetail APIs'], operation_id='patch particular cast core detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App3 : CastCoreDetail APIs'], operation_id='delete particular cast core detail',
))
class CastCoreDetail_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = CastCoreDetail.objects.select_related('cast')
    serializer_class = CastCoreDetailSerializer
