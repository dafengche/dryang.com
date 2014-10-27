"""
Django settings for apps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tb)-+qph@b(#2!&3i-v#m4fc04j7=_6gk7nr4-%e3omyhmatg8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'common.auth.apps.AuthConfig',
    'demo',
    'verif',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.broker.Broker',
)

ROOT_URLCONF = 'apps.urls'

WSGI_APPLICATION = 'apps.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# 23OCT14
# List of additional locations for
# django.contrib.staticfiles.finders.FileSystemFinder
STATICFILES_DIRS = (
    '/home/maxy/git/dev/dryang.com/common/static',
)
# Notice the default STATICFILES_FINDERS are
# django.contrib.staticfiles.finders.FileSystemFinder and
# django.contrib.staticfiles.finders.AppDirectoriesFinder

# 23OCT14
# List of locations of the template source files searched by
# django.template.loaders.filesystem.loader, in search order
TEMPLATE_DIRS = (
    '/home/maxy/git/dev/dryang.com/common/templates',
)
# Notice the default TEMPLATE_LOADERS are
# django.template.loaders.filesystem.Loader and
# django.template.loaders.app_directories.Loader


# Logging, 29SEP14
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(module)s %(process)d %(thread)d: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
#        'django': {
#            'handlers':['file'],
#            'propagate': True,
#            'level': 'INFO',
#        },
        'demo': {
#            'handlers': ['console', 'file'],
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'verif': {
#            'handlers': ['console', 'file'],
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'common.auth': {
#            'handlers': ['console', 'file'],
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}


# Celery, 30SEP14
BROKER_URL = 'amqp://mw01/'
CELERY_RESULT_BACKEND = 'redis://mw01/'
# 2OCT14
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'


# AuthN, 22OCT14
#AUTHENTICATION_BACKEND = (
#    'common.auth.backends.LDAPBackend',
##    'django.contrib.auth.backends.ModelBackend',
#)
#LDAP_SERVER_URI = 'ldap://mw01'
#LDAP_BASE_DN = 'dc=dryang,dc=com'

# AuthN related URLs
# LOGIN_REDIRECT_URL default: /accounts/profile/
# LOGIN_URL          default: /accounts/login/
# LOGOUT_URL         default: /accounts/logout/

# Make every RequestContext contain a variable "request", which is the current
# HttpRequest, 27OCT14
from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)
