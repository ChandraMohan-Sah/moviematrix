from .base import *

DEBUG = True
ALLOWED_HOSTS = ['moviematrix.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'database' /'db.sqlite3',
    }
}
