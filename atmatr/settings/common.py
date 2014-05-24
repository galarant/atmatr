import os
import atmatr.settings.secret as secret_settings

#=============== GENERAL APPLICATION SETTINGS ====================

PROJECT_NAME = 'atmatr'
BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')
SECRET_KEY = secret_settings.SECRET_KEY

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'atmatr.urls'
WSGI_APPLICATION = 'atmatr.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#=============== FRONT-END SETTINGS ====================

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + 'public/static'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR + 'public/media'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
