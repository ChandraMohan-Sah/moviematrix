from django.urls import path
from . import views
 
urlpatterns = [
    # CAST
    path('casts/', views.Cast_ListCreate_View.as_view(), name='cast-create-list'),
    # path('casts/create/', views.CastCreateView.as_view(), name='cast-create'),
    path('casts/<int:pk>/', views.Cast_RUD_View.as_view(), name='cast-detail'),

    # # CORE DETAIL
    path('cast-core-detail/', views.CastCoreDetail_ListCreate_View.as_view(), name='cast-core-detail-list-create'),
    path('cast-core-detail/<int:pk>/', views.CastCoreDetail_RUD_View.as_view(), name='cast-core-detail-detail'),

    # # KNOWN FOR
    # path('casts/known-for/', views.CastKnownForCreateView.as_view(), name='cast-knownfor-create'),
    # path('casts/known-for/list/', views.CastKnownForListView.as_view(), name='cast-knownfor-list'),
]
  