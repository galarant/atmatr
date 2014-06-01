from atmatr.settings.common import *
import atmatr.settings.secret as secret_settings

#=============== GENERAL APPLICATION SETTINGS ====================

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = INSTALLED_APPS + ['django_nose', 'debug_toolbar', ]
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ['debug_toolbar.middleware.DebugToolbarMiddleware']

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

#================ LOGGING SETTINGS =====================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.request': {
            # no desire to mail admins
            #'handlers': ['mail_admins'],
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        # logger for the atmatr namespace
        'atmatr': {

        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    }
}

# all loggers prefixed with a atmatr namespace will output to the console
# at DEBUG or higher.

LOGGING['loggers']['atmatr'] = {
    'handlers': ['console'],
    'level': 'DEBUG',
}

#================== DEBUG TOOLBAR SETTINGS =================
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
