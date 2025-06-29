
from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema_view = get_schema_view(
#    openapi.Info(
#       title="IMDB Media API",
#       default_version='v1',
#       description="API documentation",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="csah9628@email.com"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=[permissions.IsAuthenticated],
# )


schema_view = get_schema_view(
   openapi.Info(
      title="Media Platform API",
      default_version='v1',
      description=(
         "This documentation covers a modular, scalable, and production-ready media platform backend. "
         "It includes fully authenticated REST APIs built with Django and Django REST Framework, "
         "designed to support rich content services such as media listing, user authentication, search, "
         "filtering, ordering, pagination, and optimized asset delivery via CDN. "
         "The platform emphasizes clean design patterns, performance best practices, and deployment readiness "
         "for cloud-native environments."
      ),
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="csah9628@email.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.IsAuthenticatedOrReadOnly],
)

urlpatterns = [
    path('', include('home.api_of_home.urls')),
    path('admin/', admin.site.urls),
    path('app1_media_manger/', include('apps.app1_media_manger.api_of_app1_media_manger.urls')),
    path('app2_gener_platform/', include('apps.app2_gener_platform.api_of_app2_gener_platform.urls')),
    path('app3_cast/', include('apps.app3_cast.api_of_app3_cast.urls')),
    path('app4_creator/', include('apps.app4_creator.api_of_app4_creator.urls')),
    path('app5_writer/', include('apps.app5_writer.api_of_app5_writer.urls')),
    path('app6_movie/', include('apps.app6_movie.api_of_app6_movie.urls')),
    path('app7_tvshow/', include('apps.app7_tvshow.api_of_app7_tvshow.urls')),
    path('app8_lang_prod_company/', include('apps.app8_lang_prod_company.api_of_app8_lang_prod_company.urls')),
   #  path('app9_season/', include('apps.app9_season.api_of_app9_season.urls')),
    path('app10_episode/', include('apps.app10_episode.api_of_app10_episode.urls')),   

    path('account/', include('apps.user_app.api_of_user_app.urls')),
    path('user_profile/', include('apps.user_profile.api_of_user_profile.urls')),
    path('user_activity/', include('apps.user_activity.api_of_user_activity.urls')),
    path('user_preference/', include('apps.user_preference.api_of_user_preference.urls')),
    path('user_dashboard/', include('apps.user_dashboard.api_of_user_dashboard.urls')),

    path('recommendation_engine/', include('apps.recommendation_engine.api_of_recommendation_engine.urls')),
    path('collector_engine/', include('apps.collector_engine.api_of_collector_engine.urls')),
    path('bot_based_search/', include('apps.bot_based_search.api_of_bot_based_search.urls')),
    
    path('core/', include('apps.core.api_of_core.urls')),

    # Swagger and Redoc URLs
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

   #browsable login 
   path('api-auth/', include('rest_framework.urls')),
]





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




