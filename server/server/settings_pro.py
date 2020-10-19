from .settings import *
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'qkl',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': '192.168.237.10',
        'PORT': '3306',
    }
}
