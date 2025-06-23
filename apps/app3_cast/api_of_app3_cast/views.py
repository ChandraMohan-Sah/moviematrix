from app3_cast.models import Cast, CastCoreDetail, CastKnownFor
from .serializers import (
    CastSerializer,
    CastCoreDetailSerializer,
    CastKnownForSerializer
)

from app1_media_manger.api_of_app1_media_manger.serializers import CastCreateSerializer

from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import generics


#swagger docs
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator


# ------- CAST VIEWS -------
# For listing all cast entries
class CastListView(generics.ListAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer

# For creating a new cast with media
# class CastCreateView(generics.CreateAPIView):
#     queryset = Cast.objects.all() 
#     serializer_class = CastCreateSerializer 
#     parser_classes = [MultiPartParser, JSONParser]

class CastCreateView(generics.CreateAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastCreateSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        cast = serializer.save()

        # ✅ Use full serializer for output
        output_serializer = CastSerializer(cast, many=many)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    

class CastDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer


# ------- CAST CORE DETAIL -------
class CastCoreDetailCreateView(generics.CreateAPIView):
    queryset = CastCoreDetail.objects.all()
    serializer_class = CastCoreDetailSerializer


class CastCoreDetailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CastCoreDetail.objects.all()
    serializer_class = CastCoreDetailSerializer


# ------- CAST KNOWN FOR -------
class CastKnownForCreateView(generics.CreateAPIView):
    queryset = CastKnownFor.objects.all()
    serializer_class = CastKnownForSerializer


class CastKnownForListView(generics.ListAPIView):
    queryset = CastKnownFor.objects.all()
    serializer_class = CastKnownForSerializer
