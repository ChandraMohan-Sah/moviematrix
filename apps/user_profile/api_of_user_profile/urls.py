# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('update_profile/', views.UserProfileUpdateView.as_view(), name='update-profile'),
    path('fetch_users/', views.FetchAllUserProfileInfo_View.as_view(), name="fetch-all-user")
]
