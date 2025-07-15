from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app6_movie.api_of_app6_movie.serializers import MovieReadSerializer
from .recommendations import personalized_movie_recommendation


@swagger_auto_schema(
    method='get',
    operation_description="Get personalized movie recommendations for a user",
    operation_id='get personalized movie recommendations for a user [IsAuthenticated]',
    responses={200: MovieReadSerializer(many=True)},
    tags=['Recommendation Engine']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_personalized_movie_recommendation(request):
    user = request.user
    recommended = personalized_movie_recommendation(user)
    serialized = MovieReadSerializer(recommended, many=True)
    return Response(serialized.data)
 