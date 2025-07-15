from rest_framework import generics, permissions
from user_dashboard.models import UserDashboard
from .serializers import UserDashboardSerializer
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['User Dashboard'], operation_id='fetch my dashboard [IsAuthenticated]',
    operation_description='fetch my dashboard [IsAuthenticated]',
))
class UserDashboardView(generics.RetrieveAPIView):
    serializer_class = UserDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        obj, created = UserDashboard.objects.get_or_create(user=user)
        return obj
    
    