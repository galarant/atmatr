from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail

from registration.backends.simple.views import RegistrationView


class IndexView(TemplateView):

    template_name = 'index.html'


class ActivationView(RegistrationView):

    """
    Handles special behavior on registration, like sending email and setting the cookie
    """

    def post(self, request, **kwargs):
        send_mail(subject=get_template('activation_email_subject.txt').render(Context({})).strip(),
                  message=get_template('activation_email.txt').render(Context(request.POST)),
                  from_email=settings.SERVER_EMAIL,
                  recipient_list=[request.POST['email']])
        return super(ActivationView, self).post(request, **kwargs)
