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

#pagination 
from rest_framework import pagination
from shared.pagination import GlobalPagination


#permissions
from rest_framework import permissions
from shared.permissions import IsAdminOrReadOnly




# Genre views 
# ---------------------------------------------------------------------
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App2 : Genre APIs'], operation_id='create genre [IsAdminOrReadOnly]',
    operation_description='create genre [IsAdminOrReadOnly]',
))
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App2 : Genre APIs'], operation_id='fetch all genre [IsAdminOrReadOnly] [paginate-10]',
    operation_description='fetch genre [IsAdminOrReadOnly]',
))
class GenreCreateList(generics.ListCreateAPIView):
    queryset = Genre.objects.all() 
    serializer_class = GenreSerializer 
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination



 
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App2 : Genre APIs'], operation_id='retrieve particular genre detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App2 : Genre APIs'], operation_id='update particular genre detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App2 : Genre APIs'], operation_id='patch particular genre detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App2 : Genre APIs'], operation_id='delete particular genre detail [IsAdminOrReadOnly]',
))
class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all() 
    serializer_class = GenreSerializer 
    permission_classes = [IsAdminOrReadOnly]



# Platform views 
# --------------------------------------------------------------------
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App2 : Platform APIs'], operation_id='create platform [IsAdminOrReadOnly]',
    operation_description='create platform [IsAdminOrReadOnly]',
))
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App2 : Platform APIs'], operation_id='fetch all platform [paginate-10]',
    operation_description='fetch all platform [paginate-10]',
))
class PlatformListCreate(generics.ListCreateAPIView):
    queryset = Platform.objects.all() 
    serializer_class = PlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination



 
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App2 : Platform APIs'], operation_id='retrieve particular platform detail [IsAdminOrReadOnly] ',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App2 : Platform APIs'], operation_id='update particular platform detail [IsAdminOrReadOnly] ',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App2 : Platform APIs'], operation_id='patch particular platform detail [IsAdminOrReadOnly] ',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App2 : Platform APIs'], operation_id='delete particular platform detail [IsAdminOrReadOnly]',
))
class PlatformDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Platform.objects.all() 
    serializer_class = PlatformSerializer 
    permission_classes = [IsAdminOrReadOnly]

