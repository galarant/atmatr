from __future__ import absolute_import

import hashlib

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
    PageTree,
    ActionTree,
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
        """
        For now, this method just handles the initial url request from the user.
        It initializes a heirarchy of PageTree objects, scrapes the starting web page, and sends it back in the HttpResponse.
        """

        # TODO: We should definitely move this logic somewhere else very soon, but right here is fine for now
        initial_page_tree = PageTree.objects.create(user=request.user,
                                                    period=0)

        initial_action_tree = ActionTree.objects.create(page_tree=initial_page_tree,
                                                        previous_page=None,
                                                        url=request.POST['starting_page'])

        first_action = Action.objects.create(action_tree=initial_action_tree,
                                             previous_action=None,
                                             function=FunctionDef.objects.get(name='get', klass__name='webdriver.PhantomJS'))

        first_action_kwargs = ActionKwarg.objects.create(action=first_action,
                                                         arg_def=first_action.function.kwargs.get(name='url'),
                                                         value=request.POST['starting_page'])

        second_action = Action.objects.create(action_tree=initial_action_tree,
                                              previous_action=first_action,
                                              function=FunctionDef.objects.get(name='page_source', klass__name='webdriver.PhantomJS'))

        from pprint import pformat
        print """
              ========= PAGE_TREE ==========
              {0}

              ========= ACTION_TREE ========
              {1}

              ========= FIRST_ACTION =======
              {2}

              === FIRST_ACTION_CALLABLE ====
              {3}

              ========= SECOND_ACTION ======
              {4}

              === SECOND_ACTION_CALLABLE ===
              {5}

              """.format(pformat(initial_page_tree.__dict__),
                         pformat(initial_action_tree.__dict__),
                         pformat(first_action.__dict__),
                         pformat(first_action.callable_string()),
                         pformat(second_action.__dict__),
                         pformat(second_action.callable_string()))

        return super(IndexView, self).post(request, **kwargs)

    def form_valid(self, form):
        """
        Doesn't really do much right now.
        In the future it will scrape the initial URL and redirect to the ActionTree experience.
        """

        return super(IndexView, self).form_valid(form)
