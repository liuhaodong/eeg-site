"""
Django settings for EEG project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#from configurations import Configuration

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__)) + '/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i%@71-4znp%(6pu%=q%e@y=r6n^j2@1!%d_k&do!taxhw%k%c6'

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
#'django.contrib.admin',
#'oauth2_provider',
#'corsheaders',
'storages',
'EEG.account',
'EEG.API',
'EEG.myauth',
'EEG.data_store',
'EEG.debug',
'EEG.prof',
'EEG.site',
'EEG.student',
'EEG.nm',
'rest_framework',
#'rest_framework.authtoken',
#'social_auth'
)

MIDDLEWARE_CLASSES = (
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
'EEG.utils.exception.ExceptionLoggingMiddleware',
#'corsheaders.middleware.CorsMiddleware',
)
REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.SessionAuthentication',
)
}
ROOT_URLCONF = 'EEG.urls'

WSGI_APPLICATION = 'EEG.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

if os.environ.get('PROD'):
	DATABASES = {
	'default': {
	'ENGINE': 'django.db.backends.mysql',
	'NAME': os.environ['RDS_DB_NAME'],
	'USER': os.environ['RDS_USERNAME'],
	'PASSWORD': os.environ['RDS_PASSWORD'],
	'HOST': os.environ['RDS_HOSTNAME'],
	'PORT': os.environ['RDS_PORT'],
	}
	}
else:
	DATABASES = {
	'default': {
	    'ENGINE': 'django.db.backends.sqlite3',
	    'NAME': os.path.join(BASE_DIR, 'prod.sqlite3'),
	    'USER': '',
	    'PASSWORD': '',
	    'HOST': '',
	    'PORT': ''
	}
	}


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AWS_ACCESS_KEY_ID = 'AKIAJUIRM65WZQZ7ZDIQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'eeg-site-media'
AWS_QUERYSTRING_AUTH = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

MEDIA_ROOT = '/media/' 
STATIC_ROOT = '/static/'
if os.environ.get('PROD'):
	DEFAULT_FILE_STORAGE = 'EEG.s3utils.MediaRootS3BotoStorage'
	STATICFILES_STORAGE = 'EEG.s3utils.StaticRootS3BotoStorage'
	S3_URL = 'http://s3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
	MEDIA_URL = S3_URL + MEDIA_ROOT
	STATIC_URL = S3_URL + STATIC_ROOT
STATIC_URL = STATIC_ROOT
MEDIA_URL = MEDIA_ROOT

STATICFILES_DIRS = (os.path.dirname(__file__)+STATIC_ROOT,)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.SessionAuthentication',
)
}

# URL that handles the media served from MEDIA_ROOT.
MEDIAFILES_DIRS = (os.path.dirname(__file__)+MEDIA_ROOT,)
MEDIAFILES_FINDERS = (
'django.contrib.mediafiles.finders.FileSystemFinder',
'django.contrib.mediafiles.finders.AppDirectoriesFinder',
)

CORS_ORIGIN_ALLOW_ALL = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'synmetric.cmu@gmail.com'
EMAIL_HOST_PASSWORD = 'synmetric'
EMAIL_PORT = 587
