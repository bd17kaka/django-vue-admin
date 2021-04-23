from .settings import *
DEBUG = True
DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'gs',
                'USER': 'root',
                'PASSWORD': 'mysqldb',
                'HOST': '127.0.0.1',
                'PORT': '3306',
        }
}
