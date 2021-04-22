from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'backend_roc',
        'USER': 'roossst',
        'PASSWORD': 'Gloadmin@123',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
          'autocommit': True,
        },
    }
}