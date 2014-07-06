
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dkh!=y2d5@odkfngnz$(xotn=r-9(!gyddqo&u*#-!4f%t^ae!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
	TEMPLATE_DEBUG = True
else:
	TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = (
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.messages',
     'django.contrib.staticfiles',
     'eventslist',
     
)



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
    
)

ROOT_URLCONF = 'worldevents.urls'

LOGIN_URL = '/eventslist/login'

WSGI_APPLICATION = 'worldevents.wsgi.application'

#Test
TEST_RUNNER = 'worldevents.tests.MongoTestSuiteRunner'
_MONGODB_TEST_NAME = 'db_test'
TEST_MODE = False

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

_ = lambda s: s

LANGUAGES = (
    ('es', _('Espanol')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"), 
)

#S3 STORAGE

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACESS_KEY = ''
BUCKET_NAME = 'worldevents_static'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

if DEBUG:

	STATIC_URL = '/static/'

	STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

	MEDIA_ROOT=os.path.join(BASE_DIR, "static/media/")

	STORAGE = "local"

else:

	STATIC_URL = 'https://s3.amazonaws.com/worldevents_static/'

	STATICFILES_DIRS = 'https://s3.amazonaws.com/worldevents_static/'

	MEDIA_ROOT='https://s3.amazonaws.com/worldevents_static/media/'

	STORAGE = "s3"

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
	'ENGINE': ''	
    }
}

#log
LOGGING = {
    'version': 1,
}

#MongoDatabase

if DEBUG:
	_MONGODB_HOST = 'localhost'
else:
	_MONGODB_HOST = ''
		
_MONGODB_NAME = 'worldevents'
_MONGODB_DATABASE_HOST = \
    'mongodb://%s/%s' \
    % (_MONGODB_HOST, _MONGODB_NAME)

from mongoengine import connect
connect(_MONGODB_NAME, host=_MONGODB_DATABASE_HOST)

SESSION_ENGINE = 'mongoengine.django.sessions'
