from django.conf import settings
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail

from django.views.generic.base import(
    TemplateView,
    RedirectView,
)

from django.contrib.auth.decorators import(
    login_required,
    permission_required,
    user_passes_test,
)

from django.shortcuts import (
    render,
    redirect
)

from registration.backends.simple.views import RegistrationView


class AuthenticatedView(View):

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(AuthenticatedView, self).dispatch(*args, **kwargs)


class WelcomeView(TemplateView):

    template_name = 'welcome.html'


class IndexView(AuthenticatedView, TemplateView):

    template_name = 'index.html'


class ActivationView(RegistrationView):
    """
    Handles special behavior on registration, like sending email and setting the cookie
    """

    def get_success_url(self, request, user):
        """
        Provides a custom success url
        """
        return 'index'

    def post(self, request, **kwargs):
        send_mail(subject=get_template('activation_email_subject.txt').render(Context({})).strip(),
                  message=get_template('activation_email.txt').render(Context(request.POST)),
                  from_email=settings.SERVER_EMAIL,
                  recipient_list=[request.POST['email']])
        return super(ActivationView, self).post(request, **kwargs)

class DeactivationView(RedirectView):
    """
    Deactivates the user if they have the proper code
    """

    permanent = False
    pattern_name = 'welcome'

    def get(self, request, **kwargs):
        print "I AM PROCESSING THE GET REQUEST"
        try:
            if kwargs['deactivation_code'] == request.user.password:
                request.user.is_active = False
                request.user.save()
            else:
                print "BAD CODE. USER NOT DEACTIVATED"
        except (AttributeError, KeyError):
            print "CANNOT DEACTIVATE ANONYMOUS USER"
            pass
        return super(DeactivationView, self).get(request, **kwargs)
