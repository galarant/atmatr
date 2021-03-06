from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

from django.views.generic.base import RedirectView
from atmatr.apps.frontend.views import (
    IndexView,
    WelcomeView,
    ActivationView,
    DeactivationView,
    ScriptView,
)

urlpatterns = patterns(url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^welcome/$', WelcomeView.as_view(), name='welcome'),
                       url(r'^script/(?P<starting_url>.*)/$', ScriptView.as_view(), name='script'),
                       url(r'^accounts/register/$', ActivationView.as_view(), name='register'),
                       url(r'^accounts/deactivate/$', DeactivationView.as_view(), name='deactivate'),
                       url(r'^accounts/', include('registration.backends.simple.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
