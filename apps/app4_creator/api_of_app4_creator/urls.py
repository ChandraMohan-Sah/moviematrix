# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('creators/', views.Creator_ListCreate_View.as_view(), name="creator-list-create"),
    path('creators/<int:pk>/', views.Creator_RUD_View.as_view(), name="creator-detail" ),


    # CORE DETAIL
    path('creator-core-detail/', views.CreatorCoreDetail_ListCreate_View.as_view(), name='creator-core-detail-list-create'),
    path('creator-core-detail/<int:pk>/', views.CreatorCoreDetail_RUD_View.as_view(), name='creator-core-detail-detail'),

]
