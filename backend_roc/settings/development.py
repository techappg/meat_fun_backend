from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'backend_roc',
        'USER': 'root',
        'PASSWORD':'Gloadmin@123',
        'HOST': '167.86.124.9',
        'PORT': '3306',
        # 'OPTIONS': {
        #   'autocommit': True,
        # },
    }
}
