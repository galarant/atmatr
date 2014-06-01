from atmatr.settings.common import *
import atmatr.settings.secret as secret_settings

#=============== GENERAL APPLICATION SETTINGS ====================

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = INSTALLED_APPS + ['django_nose', 'debug_toolbar',]
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
