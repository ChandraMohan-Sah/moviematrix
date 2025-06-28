# urls.py
from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
# from user_app.api_of_user_app.views import registration_view

urlpatterns = [
    path('login/', ObtainAuthToken.as_view(), name='api_token_auth'),  # Token-based authentication endpoint
    path('register/', views.registration_view, name='registration_view'),  # User registration endpoint
    path('logout/', views.logout_view, name='logout'),  # User logout endpoint
]


'''
login/
    headers:
        username     cms 
        password     admin

logout/ 
    headers:
        Authorization   Token asfljsndfljkbsndfljdfvds

register/
    body :
        form-data : 
            username 
            email 
            password 
            confirm_password 



'''