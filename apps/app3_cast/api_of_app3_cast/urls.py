from django.urls import path
from . import views

urlpatterns = [
    # CAST
    path('casts/', views.CastListView.as_view(), name='cast-list'),
    path('casts/create/', views.CastCreateView.as_view(), name='cast-create'),
    path('casts/<int:pk>/', views.CastDetailView.as_view(), name='cast-detail'),

    # CORE DETAIL
    path('casts/core-detail/', views.CastCoreDetailCreateView.as_view(), name='cast-core-create'),
    path('casts/core-detail/<int:pk>/', views.CastCoreDetailDetailView.as_view(), name='cast-core-detail'),

    # KNOWN FOR
    path('casts/known-for/', views.CastKnownForCreateView.as_view(), name='cast-knownfor-create'),
    path('casts/known-for/list/', views.CastKnownForListView.as_view(), name='cast-knownfor-list'),
]
