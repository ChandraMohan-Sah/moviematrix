import os
import sys
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Add custom apps to path
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

SECRET_KEY = config('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    # object storage 
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',

    # Custom apps
    'app1_media_manger',
    'app2_gener_platform',
    'app3_cast',
    'app4_creator',
    'app5_writer',
    'app6_movie',
    'app7_tvshow',
    'app8_lang_prod_company',
    'app9_season',
    'app10_episode',

    'user_app',
    'user_profile',
    'user_activity',
    'user_preference',
    'user_dashboard',

    'recommendation_engine',
    'collector_engine',
    'bot_based_search',
    'core',
    
    'home',

    # django restframework
    'rest_framework',

    # django filter
    'django_filters',

    # swagger
    'drf_yasg',

    #authentication
    'rest_framework.authtoken',

    # Django Documentation
    'docs',

    # Django Silk
    'silk',

    # django debug
    'debug_toolbar',

    # django-extensions
    'django_extensions',

    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # django-silk
    'silk.middleware.SilkyMiddleware',
    # django-debug
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUD_NAME'),
    'API_KEY': config('API_KEY'),
    'API_SECRET': config('API_SECRET')
}


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
 


REST_FRAMEWORK = {
    # token authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    # filtering 
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

# For token authentication in swagger UI
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Token-based auth using `Token <your_token>`",
        }
    },
}

# caching
CACHES = {
   'default': {
      'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
      'LOCATION': 'cached_table',
   }
}

# django silk setup
SILKY_PYTHON_PROFILER = True
SILKY_INTERCEPT_PERCENT = 100  # profile all requests

# django debug toolbar setup
INTERNAL_IPS = [
    "127.0.0.1",
]

# Sphinix Documentaion Configuration
DOCS_ROOT = os.path.join(BASE_DIR, '../docs/_build/html')
DOCS_ACCESS = 'staff'


