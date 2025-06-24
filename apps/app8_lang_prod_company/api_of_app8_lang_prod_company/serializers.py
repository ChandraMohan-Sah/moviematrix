# serializers.py
from rest_framework import serializers 
from app8_lang_prod_company.models import Language , ProductionCompany


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
    

class ProductionCompanySerializer(serializers.ModelSerializer):
    class Meta: 
        model = ProductionCompany
        fields = '__all__'

