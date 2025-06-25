# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('writers/', views.Writer_ListCreate_View.as_view(), name="writer-list-create"),
    path('writer/<int:pk>/', views.Writer_RUD_View.as_view(), name="writer-rud"),

    path('writercoredetail/', views.WriterCoreDetail_ListCreate_View.as_view(), name="writercoredetail-list-create"),
    path('writercoredetail/<int:pk>/', views.WriterCoreDetail_RUD_View.as_view(), name="writer-rud")
    
]
