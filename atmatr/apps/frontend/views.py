import hashlib

from django.conf import settings
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives

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

from django.contrib.auth.models import User

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
        mail_context = request.POST.copy()
        mail_context['deactivation_code'] = hashlib.md5(mail_context['username']).hexdigest()
        mail_context['http_host'] = request.META['HTTP_HOST']
        msg = EmailMultiAlternatives(subject=get_template('activation_email_subject.txt').render(Context({})).strip(),
                                     body=get_template('activation_email.txt').render(Context(mail_context)),
                                     from_email=settings.SERVER_EMAIL,
                                     to=[request.POST['email']])
        msg.attach_alternative(get_template('activation_email.txt').render(Context(mail_context)), "text/html")
        msg.send()
        return super(ActivationView, self).post(request, **kwargs)


class DeactivationView(RedirectView):

    """
    Deactivates the user if they have the proper code
    """

    permanent = False
    pattern_name = 'welcome'

    def get(self, request, **kwargs):
        code = request.GET.get('code')
        if code:
            # this is really stupid but I don't want to extend the User model right now
            for user in User.objects.all():
                user_code = hashlib.md5(user.username).hexdigest()
                if user_code == code:
                    user.is_active = False
                    user.save()
        return super(DeactivationView, self).get(request, **kwargs)
