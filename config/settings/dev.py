# flake8: noqa
from config.settings.base import *

SECRET_KEY = 'not so secret, only used for docker commands locally'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': get_env_variable('PSQL_HOST'),
        'NAME': get_env_variable('PSQL_NAME'),
        'USER': get_env_variable('PSQL_USERNAME'),
        'PASSWORD': get_env_variable('PSQL_PASSWORD'),
    }
}

INSTALLED_APPS += [
    'django_extensions',
]
