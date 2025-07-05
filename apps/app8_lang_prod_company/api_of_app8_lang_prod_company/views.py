from rest_framework import generics
from app8_lang_prod_company.models import Language, ProductionCompany
from .serializers import (
    LanguageSerializer,
    ProductionCompanySerializer
)

# swagger docs 
from drf_yasg.utils import swagger_auto_schema 
from django.utils.decorators import method_decorator 

# permissions
from shared.permissions import IsAdminOrReadOnly

# Pagination 
from shared.pagination import GlobalPagination


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App8 : Language APIs'], operation_id='list all  languages available [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all  languages available [IsAdminOrReadOnly] [Paginate-10]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App8 : Language APIs'], operation_id='create a language [IsAdminOrReadOnly]',
    operation_description='create a language [IsAdminOrReadOnly]',
)) 
class Language_CreateList_View(generics.ListCreateAPIView):
    queryset = Language.objects.all() 
    serializer_class = LanguageSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App8 : Language APIs'], operation_id='retrieve particular language detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App8 : Language APIs'], operation_id='update particular language detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App8 : Language APIs'], operation_id='patch particular language detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App8 : Language APIs'], operation_id='delete particular language detail [IsAdminOrReadOnly]',
))
class Language_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAdminOrReadOnly]
    


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App8 : Production Company APIs'], operation_id='list all production company  available [IsAdminOrReadOnly] [Paginate-10]',
    operation_description='list all production company  available [IsAdminOrReadOnly] [Paginate-10]',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App8 : Production Company APIs'], operation_id='create a production company [IsAdminOrReadOnly]',
    operation_description='create a production company [IsAdminOrReadOnly]',
)) 
class ProductionCompany_CreateList_View(generics.ListCreateAPIView):
    queryset = ProductionCompany.objects.all() 
    serializer_class = ProductionCompanySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = GlobalPagination



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App8 : Production Company APIs'], operation_id='retrieve particular production company  detail [IsAdminOrReadOnly]',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App8 : Production Company APIs'], operation_id='update particular  production company  detail [IsAdminOrReadOnly]',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App8 : Production Company APIs'], operation_id='patch particular  production company  detail [IsAdminOrReadOnly]',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App8 : Production Company APIs'], operation_id='delete particular  production company  detail [IsAdminOrReadOnly]',
))
class ProductionCompany_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductionCompany.objects.all()
    serializer_class = ProductionCompanySerializer
    permission_classes = [IsAdminOrReadOnly] 


