from .base import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']  # replace with your actual domain

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # example
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
