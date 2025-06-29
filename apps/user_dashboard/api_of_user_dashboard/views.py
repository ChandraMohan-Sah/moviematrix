# views.py
from .serializers import UserDashboardSerializer 
from rest_framework import generics, permissions
from user_dashboard.models import UserDashboard


# swagger docs 
from drf_yasg.utils import swagger_auto_schema 
from django.utils.decorators import method_decorator 


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['User Dashboard'], operation_id='fetch all user information',
    operation_description='fetch all user information', 
))
class UserDashboardView(generics.ListAPIView):
    queryset = UserDashboard.objects.all()
    serializer_class = UserDashboardSerializer 
    permission_classes = [permissions.IsAuthenticated]

