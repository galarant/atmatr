from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.views.generic.base import RedirectView
from atmatr.apps.frontend.views import IndexView

urlpatterns = patterns((r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^admin/', include(admin.site.urls)),
                       )
