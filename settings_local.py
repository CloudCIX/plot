# Local settings that change on a per application / per environment basis
import os

PGSQLAPI_PASSWORD = os.getenv('PGSQLAPI_PASSWORD', 'pw')
PGSQLAPI_USER = os.getenv('PGSQLAPI_USER', 'postgres')
PGSQLAPI_HOST = os.getenv('PGSQLAPI_HOST', 'pgsqlapi')
POD_NAME = os.getenv('POD_NAME', 'pod')
ORGANIZATION_URL = os.getenv('ORGANIZATION_URL', 'example.com')

ALLOWED_HOSTS = [
    f'plot.{POD_NAME}.{ORGANIZATION_URL}',
]
if os.getenv('NGINX_IPV4', '') != '':
    ALLOWED_HOSTS.append(os.getenv('NGINX_IPV4'))
if os.getenv('NGINX_IPV6', '') != '':
    ALLOWED_HOSTS.append(os.getenv('NGINX_IPV6'))

ALLOWED_HOSTS = tuple(ALLOWED_HOSTS)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'plot': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'plot',
        'USER': PGSQLAPI_USER,
        'PASSWORD': PGSQLAPI_PASSWORD,
        'HOST': PGSQLAPI_HOST,
        'PORT': '5432',
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_default',
        'USER': PGSQLAPI_USER,
        'PASSWORD': PGSQLAPI_PASSWORD,
        'HOST': PGSQLAPI_HOST,
        'PORT': '5432',
    },
}

DATABASE_ROUTERS = [
    'plot.db_router.PlotRouter',
]

INSTALLED_APPS = [
    'plot',
]

# Localisation
USE_I18N = False
USE_L10N = False

ORG = ORGANIZATION_URL.split('.')[0]

APPLICATION_NAME = os.getenv('APPLICATION_NAME', f'{POD_NAME}_{ORG}_plot')
CLOUDCIX_INFLUX_TAGS = {
    'service_name': APPLICATION_NAME,
}
