# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('update_profile/', views.UserProfileUpdateView.as_view(), name='update-profile'),
    path('fetch_users/', views.UserProfileInfoView.as_view(), name="fetch-all-user")
]
