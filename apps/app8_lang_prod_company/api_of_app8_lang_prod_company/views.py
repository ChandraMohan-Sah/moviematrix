from rest_framework import generics
from app8_lang_prod_company.models import Language, ProductionCompany
from .serializers import (
    LanguageSerializer,
    ProductionCompanySerializer
)

# swagger docs 
from drf_yasg.utils import swagger_auto_schema 
from django.utils.decorators import method_decorator 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App8 : Language APIs'], operation_id='list all  languages available',
    operation_description='list all  languages available',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App8 : Language APIs'], operation_id='create a language',
    operation_description='create a language',
)) 
class Language_CreateList_View(generics.ListCreateAPIView):
    queryset = Language.objects.all() 
    serializer_class = LanguageSerializer




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App8 : Language APIs'], operation_id='retrieve particular language detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App8 : Language APIs'], operation_id='update particular language detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App8 : Language APIs'], operation_id='patch particular language detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App8 : Language APIs'], operation_id='delete particular language detail',
))
class Language_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App8 : Production Company APIs'], operation_id='list all production company  available',
    operation_description='list all production company  available',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['App8 : Production Company APIs'], operation_id='create a production company',
    operation_description='create a production company',
)) 
class ProductionCompany_CreateList_View(generics.ListCreateAPIView):
    queryset = ProductionCompany.objects.all() 
    serializer_class = ProductionCompanySerializer



@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['App8 : Production Company APIs'], operation_id='retrieve particular production company  detail',
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['App8 : Production Company APIs'], operation_id='update particular  production company  detail',
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['App8 : Production Company APIs'], operation_id='patch particular  production company  detail',
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=['App8 : Production Company APIs'], operation_id='delete particular  production company  detail',
))
class ProductionCompany_RUD_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductionCompany.objects.all()
    serializer_class = ProductionCompanySerializer
