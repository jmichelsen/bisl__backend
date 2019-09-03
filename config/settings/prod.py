# flake8: noqa
import django_heroku
import dj_database_url

from config.settings.base import *

DEBUG = get_env_variable('PROD_DEBUG', False)
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['localhost', '.bisl.com', 'www.bisl.com', 'bisl.herokuapp.com']

CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = bool(get_env_variable('DJANGO_SSL_REDIRECT', default=False))
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_HOST = 'bisl.com'

# Database
# Heroku: Update database configuration from $DATABASE_URL.
DATABASES = {'default': dj_database_url.config(conn_max_age=500)}

django_heroku.settings(locals(), logging=False, staticfiles=False)
