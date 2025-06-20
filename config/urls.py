"""
URL configuration for moviematrix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
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
    path('user_app/', include('apps.user_app.api_of_user_app.urls')),
    path('user_profile/', include('apps.user_profile.api_of_user_profile.urls')),
    path('user_activity/', include('apps.user_activity.api_of_user_activity.urls')),
    path('user_preference/', include('apps.user_preference.api_of_user_preference.urls')),
    path('user_dashboard/', include('apps.user_dashboard.api_of_user_dashboard.urls')),
    path('recommendation_engine/', include('apps.recommendation_engine.api_of_recommendation_engine.urls')),
    path('collector_engine/', include('apps.collector_engine.api_of_collector_engine.urls')),
    path('bot_based_search/', include('apps.bot_based_search.api_of_bot_based_search.urls')),
    path('core/', include('apps.core.api_of_core.urls')),
]





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




