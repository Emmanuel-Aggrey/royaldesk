"""
Django settings for HRMSPROJECT project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import pyodbc
from datetime import datetime
from decouple import config
from django.core import management
from django.conf import settings

# import django_heroku
# import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*', '9ccf-154-160-6-247.eu.ngrok.io/',
                 '9ccf-154-160-6-247.eu.ngrok.io']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'django.contrib.staticfiles',
    'django.contrib.humanize',


    # LOCALS APPS
    'BaseModel',
    'hrms',
    'helpdesk',
    'applicant',

    # 3RD PARTY APPS
    'rest_framework',
    'drf_yasg',
    'debug_toolbar',
    'ckeditor',
    "corsheaders",

    'django_celery_results',
    'djcelery_email',
    'django_celery_beat',
    'auditlog',
    'dbbackup',
    # 'django_model_changes',



]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'HRMSPROJECT.applicantUserMiddleware.ApplicantUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',

]

ROOT_URLCONF = 'HRMSPROJECT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'hrms.context_preporsessor.sql_server_is_connected',
                'hrms.context_preporsessor.no_beneficiaries',
                'hrms.context_preporsessor.company_name',
                

            ],
        },
    },
]

WSGI_APPLICATION = 'HRMSPROJECT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Development


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRESS_HOST'),
        'PORT': config('POSTGRESS_PORT'),
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


AUTH_USER_MODEL = 'helpdesk.User'
# Production





# this will update settings datbase configuration automatically from heroku and let us local config also


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/




# FORCE_SERVE_STATIC = True

STATIC_ROOT =  os.path.join(BASE_DIR, 'staticfile')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]



# '/media/' #This is just for url i.e https://l.me/media/l.jpg
MEDIA_URL = '/media/'
# os.path.join(BASE_DIR, 'media') #This is the folder the image will be uploaded
MEDIA_ROOT  =  os.path.join(BASE_DIR, 'media')


CKEDITOR_UPLOAD_PATH = "uploads/"


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# CELERY_EMAIL_BACKEND =  'djcelery_email.backends.CeleryEmailBackend'

# EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
CELERY_EMAIL_CHUNK_SIZE = 1
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
HR_EMAIL = config('HR_EMAIL')



# email used for testing in production
TEST_EMAIL = config('TEST_EMAIL')

# ERROR MAILS SENT TO ADMINS EMAIL
SERVER_EMAIL = config('TEST_EMAIL')


# SETTING UP CELERY
CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_BROKER_URL = 'amqp://localhost'
# CELERY_RESULT_BACKEND = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# STORE RESULTS IN DJANGO DB
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
# celery setting.
# CELERY_CACHE_BACKEND = 'default'
BROKER_POOL_LIMIT=0


# CACHE setting.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'celery_cache_table',
    }
}


# CELERY BEAT SETTINGS
CELERYBEAT_SCHEDULE = 'django_celery_beat.schedulers:DatabaseScheduler'


CSRF_TRUSTED_ORIGINS = [config('CSRF_TRUSTED_ORIGINS')]



DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': config('DBBACKUP_LOCATION')}



# DJANGO MODEL LOGS
AUDITLOG_INCLUDE_ALL_MODELS= config('AUDITLOG_MODELS', default=False, cast=bool)


# DJANGO DEBUG TOOLBAR
INTERNAL_IPS = ('127.0.0.1',)

CORS_ORIGIN_ALLOW_ALL = True


# CORS_ALLOWED_ORIGINS = [
# "http://localhost:8000",
# "http://127.0.0.1:8000",
# "http://192.168.1.18",
# ]