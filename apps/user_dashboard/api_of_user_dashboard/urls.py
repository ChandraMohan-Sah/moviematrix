# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('user_dashboard/', views.UserDashboardView.as_view(), name="user-dashboard")
]


