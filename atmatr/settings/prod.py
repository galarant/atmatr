from atmatr.settings.common import *
import atmatr.settings.secret as secret_settings

#=============== GENERAL APPLICATION SETTINGS ====================

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = INSTALLED_APPS + ['django_nose',]

EMAIL_HOST = 'mailtrap.io'
EMAIL_HOST_USER = secret_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secret_settings.EMAIL_HOST_PASSWORD
EMAIL_PORT = 2525
EMAIL_USE_TLS = False

ADMINS = [('Jeff Revesz', 'kingmobwashere@gmail.com'), ]
SERVER_EMAIL = 'Automator Notifications <no_reply@atmatr.com>'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'atmatr',
        'USER': 'atmatr',
        'PASSWORD': secret_settings.DEFAULT_DATABASE_PASSWORD,
        'HOST': 'localhost',
        'ATOMIC_REQUESTS': True,
    }
}
