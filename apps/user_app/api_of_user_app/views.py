# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from user_app.api_of_user_app.serializers import RegistrationSerializer


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
 

@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        try: 
            request.user.auth_token.delete() 
            return Response({"message":"Logout Successfully"}, status=200)
        
        except (AttributeError, Token.DoesNotExist):
            return Response({
                "error":"Invalid token or user not authenticated"
            }, status = 401)
  
 

@swagger_auto_schema(
    method='post',
    request_body=RegistrationSerializer,  #  this is what enables the payload form
    operation_description="👥 Register a new user",
    # operation_summary="User Registration",
    tags=['👥 User Registration '],
    responses={200: openapi.Response('Registration success')}
)
@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save() 
            data['response'] = "Registration Successful"
            data['username'] = account.username 
            data['email'] = account.email 

            token = Token.objects.get(user=account).key 
            data['token'] = token 
            return Response(
                data, 
                status=status.HTTP_201_CREATED
            )

        else: 
            # If the serializer is not valid, return the errors
            # This will return a 400 Bad Request response with the error details
            return Response(serializer.errors, status = 400)
        
