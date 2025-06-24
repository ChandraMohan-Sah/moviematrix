# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('languages/', views.Language_CreateList_View.as_view(), name="language-create-list"),
    path('languages/<int:pk>/', views.Language_RUD_View.as_view(), name='languages-rud'),

    path('production_company/', views.ProductionCompany_CreateList_View.as_view(), name='production-create-list'),
    path('production_company/<int:pk>/', views.ProductionCompany_RUD_View.as_view(), name='production-rud'),
]
