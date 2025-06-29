# views.py
from rest_framework import generics, permissions
from user_profile.models import UserProfile 
from user_profile.api_of_user_profile.serializers import ( 
    UserProfileSerializer, CompleteUserProfileInfoSerializer
)

# swagger docs 
from drf_yasg.utils import swagger_auto_schema 
from django.utils.decorators import method_decorator 



@method_decorator(name='put', decorator=swagger_auto_schema(
    tags=['User Profile'], operation_id='update user profile pic',
    operation_description='update user profile pic', 
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    tags=['User Profile'], operation_id='update user profile pci',
    operation_description='update user profile pic', 
))
class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer 
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile  #related_name='profile'




@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['User Profile'], operation_id='fetch all user information',
    operation_description='fetch all user information', 
))
class UserProfileInfoView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = CompleteUserProfileInfoSerializer
    permission_classes = [permissions.IsAdminUser]

