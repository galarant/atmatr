import json as python_json

from django.db import models
from django.contrib.auth.models import User
from atmatr.models import (
    ucModel,
    TimestampModel,
    ExtendedModel,
    DateRangeModel,
)

from ..scraper.models import(
    FunctionDef,
    ArgDef,
    KwargDef,
)

from bs4 import(
    BeautifulSoup,
)

from bs4.element import Tag as bs4_Tag

from selenium import webdriver


# SUPPORT CLASSES

class Page(BeautifulSoup):

    """
    A BeautifulSoup child class that adds a custom JSON serializer
    """

    @property
    def json(self):

        """
        Serializes the soup into a JSON object with only the attributes that are important for our app
        """

        def dictify_tag(tag):

            """
            Turns a tag into a dict, keeping only the attributes we are interested in
            Recursively adds the tag's children as well
            """
            ALLOWED_TAGS = [t.name for t in Tag.objects.all()]
            SHOW_CONTENT = [t.name for t in Tag.objects.filter(show_content=True)]

            return {'name': tag.name,
                    'namespace': tag.namespace,
                    'attrs': tag.attrs,
                    'contents': str(tag.contents) if tag.name in SHOW_CONTENT else None,
                    'children': [dictify_tag(child) for child in tag.children
                                    if type(child) == bs4_Tag and child.name in ALLOWED_TAGS]}

        if not getattr(self, '_json'):
            if not self.find('html'):
                raise AttributeError("Cannot serialize: missing html tag")
            tag_as_json = python_json.dumps(dictify_tag(self.find('html')))
            self._json = tag_as_json

        return self._json


# APPLICATION MODELS

class PageTree(ExtendedModel):

    """
    This model represents the tree of pages to traverse during playback.
    Each page in the tree is represented by an ActionTree object, which is 1:M with PageTree.
    """

    user = models.ForeignKey(User, related_name="page_trees")
    period = models.FloatField()  # Amount of time between successive playbacks, in seconds


class Tag(ExtendedModel):

    """
    This model represents an HTML tag type
    http://www.w3schools.com/tags/
    """
    show_content = models.BooleanField(default=True)


class ActionTree(ExtendedModel):

    """
    This model represents a tree of actions to take on a single web page.
    During playback, pages themselves are traversed in a tree-like structure, so this model is self-referential.
    Each action in the ActionTree is represented by an Action object, which is 1:M with ActionTree.
    """

    page_tree = models.ForeignKey(PageTree, related_name="action_trees")
    previous_page = models.ForeignKey('self', null=True, blank=True, related_name="next_pages")
    url = models.URLField(max_length=2048)


    @property
    def webdriver(self):

        """
        Initializes a webdriver session for this object if one does not already exist
        Navigates the webdriver to the object's url
        """

        if not self.url:
            raise AttributeError('Cannot initialize webdriver: missing url')

        if not hasattr(self, '_selenium_session'):
            self._webdriver = webdriver.PhantomJS()
            self._webdriver.get(self.url)

        return self._webdriver

    @property
    def page(self):

        """
        Retrieves the page for this object if one does not already exist
        """

        if not hasattr(self, '_page'):
            self._page = Page(self.webdriver.page_source, 'html.parser')

        return self._page


class Action(ExtendedModel):

    """
    This model represents a single atomic action to take on a web page.
    During playback, Actions are traversed in a tree-like structure, so this model is self-referential.
    Possible Action types are limited to a subset of automatable actions supported by the selenium Python bindings.
    """

    action_tree = models.ForeignKey(ActionTree, related_name="actions")
    previous_action = models.ForeignKey('self', null=True, blank=True, related_name="next_actions")
    function = models.ForeignKey(FunctionDef)

    def klass_instance(self):
        """
        Returns an instance of self.function.klass
        """

        return eval("%s()" % self.function.klass.name) if self.function.klass else None

    def args_string(self):
        """
        Returns a string-formatted list of the action's positional arguments
        """
        my_ordered_vals = sorted(self.args.all(), key=lambda v: v.arg_def.position)

        return ",".join([v.value for v in my_ordered_vals])

    def kwargs_string(self):
        """
        Returns a string-formatted list of the action's keyword arguments
        """

        return ",".join(['{0}={1}'.format(kwarg.arg_def.name, kwarg.value) for kwarg in self.kwargs.all()])

    def callable_string(self):
        """
        Forms a callable string from the action
        """

        if self.function.klass and self.function.is_method == False:
            return self.function.name

        return '{0}({1}{2}{3})'.format(self.function.name,
                                       ", " if (self.kwargs.all() and self.args.all()) else "",
                                       self.args_string(),
                                       self.kwargs_string())


class ActionArg(ucModel, TimestampModel):

    """
    This model represents a positional argument value for a single action.
    """

    action = models.ForeignKey(Action, related_name="args")
    arg_def = models.ForeignKey(ArgDef, related_name="+")
    value = models.CharField(max_length=2048)  # The values stored here should be strictly limited to JSON-translatable strings of type self.arg_def.data_type


class ActionKwarg(ExtendedModel):

    """
    This models represents a keyword argument value for a single action.
    """

    action = models.ForeignKey(Action, related_name="kwargs")
    arg_def = models.ForeignKey(KwargDef, related_name="+")
    value = models.CharField(max_length=2048)  # The values stored here should be strictly limited to JSON-translatable strings of type self.arg_def.data_type
