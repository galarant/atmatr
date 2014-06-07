from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from django.views.generic.base import RedirectView
from atmatr.apps.frontend.views import (
    IndexView,
    WelcomeView,
    ActivationView,
    DeactivationView,
)

urlpatterns = patterns((r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^welcome/$', WelcomeView.as_view(), name='welcome'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/register/$', ActivationView.as_view()),
                       url(r'^accounts/deactivate/$', DeactivationView.as_view()),
                       url(r'^accounts/', include('registration.backends.simple.urls')),
                       )
