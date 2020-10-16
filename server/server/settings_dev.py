from .settings import *
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aishare',
        'USER': 'root',
        'PASSWORD': '971031',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
