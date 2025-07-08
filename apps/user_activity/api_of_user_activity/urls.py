# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get_user_activity/', views.get_user_activity, name='get-user-activity')
]


