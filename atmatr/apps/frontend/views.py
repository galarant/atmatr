from __future__ import absolute_import
import hashlib

from django.conf import settings
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives

from django.views.generic.base import(
    View,
    TemplateView,
    RedirectView,
)

from django.views.generic.edit import FormView

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

from .forms import(
    IndexForm,
)


class AuthenticatedView(View):

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(AuthenticatedView, self).dispatch(*args, **kwargs)


class WelcomeView(TemplateView):

    """
    A simple Welcome page for anonymous users
    """

    template_name = 'welcome.html'


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


class IndexView(AuthenticatedView, FormView):

    """
    Starts the user experience.
    This logic will probably be moved somewhere else once the project becomes less linear
    """

    template_name = 'index.html'
    form_class = IndexForm
    success_url = '/'

    def post(self, request, **kwargs):
        print "GOT THE URL: %s" % request.POST['starting_page']
        return super(IndexView, self).post(request, **kwargs)

    def form_valid(self, form):
        """
        Doesn't really do much right now.
        In the future it will scrape the initial URL and redirect to the ActionTree experience.
        """
        return super(IndexView, self).form_valid(form)
