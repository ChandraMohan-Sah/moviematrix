# views.py
from django.shortcuts import render
from django.http import HttpResponse

from app2_gener_platform.models import Genre, Platform 
from .serializers import GenreSerializer, PlatformSerializer 

from rest_framework import generics 
from rest_framework.response import Response 


#swagger docs
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator



# Genre views 
# ---------------------------------------------------------------------
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App2 : Genre APIs'], operation_id='create genre',
    operation_description='create genre',
))
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App2 : Genre APIs'], operation_id='fetch all genre',
    operation_description='fetch genre',
))
class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all() 
    serializer_class = GenreSerializer 



 
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App2 : Genre APIs'], operation_id='retrieve particular genre detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App2 : Genre APIs'], operation_id='update particular genre detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App2 : Genre APIs'], operation_id='patch particular genre detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App2 : Genre APIs'], operation_id='delete particular genre detail',
))
class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all() 
    serializer_class = GenreSerializer 



# Platform views 
# --------------------------------------------------------------------
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App2 : Platform APIs'], operation_id='create platform',
    operation_description='create platform',
))
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App2 : Platform APIs'], operation_id='fetch all platform',
    operation_description='fetch all platform',
))
class PlatformList(generics.ListCreateAPIView):
    queryset = Platform.objects.all() 
    serializer_class = PlatformSerializer



 
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App2 : Platform APIs'], operation_id='retrieve particular platform detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App2 : Platform APIs'], operation_id='update particular platform detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App2 : Platform APIs'], operation_id='patch particular platform detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App2 : Platform APIs'], operation_id='delete particular platform detail',
))
class PlatformDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Platform.objects.all() 
    serializer_class = PlatformSerializer 

