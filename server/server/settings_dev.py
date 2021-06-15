from .settings import *
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aishare',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '10.201.200.222',
        'PORT': '3306',
    }
}
