from .settings import *
# from django.db.backends.mysql.base import DatabaseWrapper
# from django.db.backends.postgresql.base import
# DatabaseWrapper.data_types['DateTimeField'] = 'datetime'
# from django_filters.utils import
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aishare',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        # 'OPTIONS': {'isolation_level': None}
    }
}
