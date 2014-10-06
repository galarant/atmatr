from __future__ import absolute_import

import hashlib
import urllib
import json

#====== DJANGO IMPORTS ======
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

#====== THIRD PARTY IMPORTS ======
from registration.backends.simple.views import RegistrationView

from selenium import webdriver

#====== PROJECT IMPORTS ======
from .forms import(
    IndexForm,
)

from .models import(
    Script,
    Page,
    Action,
    ActionArg,
    ActionKwarg,
)

from ..scraper.models import(
    FunctionDef,
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

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        if code:
            # this is really stupid but I don't want to extend the User model right now
            for user in User.objects.all():
                user_code = hashlib.md5(user.username).hexdigest()
                if user_code == code:
                    user.is_active = False
                    user.save()
        return super(DeactivationView, self).get(request, *args, **kwargs)


class IndexView(FormView, AuthenticatedView):

    """
    Starts the user experience by prompting for an initial URL
    """

    template_name = 'index.html'
    form_class = IndexForm
    success_url = '/'

    def form_valid(self, form):
        """
        Redirect to the script-creation experience
        """

        return redirect('script', starting_url=urllib.quote(self.request.POST.get('starting_url')))


class ScriptView(TemplateView, AuthenticatedView):

    """
    Leads the user through an experiece that creates a Script for offline automation
    """

    template_name = 'script.html'

    def get(self, request, *args, **kwargs):
        """
        This should only be called once, at the beginning of the Script creation process.
        We are redirected here from IndexView with a starting_url.
        """

        if not kwargs.get('starting_url'):
            # We do not belong here if we don't have a starting URL. Send the user back to IndexView
            redirect('index')

        # Otherwise we initialize a new Script model for the user, and start the script-creation experience
        new_script = Script.objects.create(user=self.request.user,
                                           period=0)

        self.page = Page.objects.create(script=new_script,
                                        parent=None,
                                        url=urllib.unquote(kwargs['starting_url']))
        return super(ScriptView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Sets the context for the template.
        This template renders an interactive treemap of the requested page
        """

        context = super(ScriptView, self).get_context_data(**kwargs)
        context['viewport_width'] = self.page.VIEWPORT_SIZE[0]
        context['viewport_height'] = self.page.VIEWPORT_SIZE[1]
        context['page_width'] = self.page.size[0]
        context['page_height'] = self.page.size[1]
        context['screenshot'] = self.page.screenshot
        return context
