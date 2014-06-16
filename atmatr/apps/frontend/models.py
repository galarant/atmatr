from decimal import Decimal

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

from selenium import webdriver

from bs4 import BeautifulSoup

from bs4.element import Tag as bs4_Tag, NavigableString

# APPLICATION MODELS


class Script(ExtendedModel):

    """
    This model represents the tree of pages to traverse during playback.
    Each page in the tree is represented by an Page object, which is 1:M with Script.
    """

    user = models.ForeignKey(User)
    period = models.FloatField()  # Amount of time between successive playbacks, in seconds


class Tag(ExtendedModel):

    """
    This model represents an HTML tag type
    http://www.w3schools.com/tags/
    """
    TAG_CATEGORIES = (('basic', 'basic'),
                      ('s_format', 's_format'),
                      ('s_format_root', 's_format_root'),
                      ('u_format', 'u_format'),
                      ('content', 'content'),
                      ('interactable', 'interactable'),)
    category = models.CharField(max_length=50, choices=TAG_CATEGORIES)


class Page(ExtendedModel):

    """
    This model represents a web page.
    During playback of a script, Pages are traversed in a tree-like structure, so this model is self-referential.
    Each action in the Page is represented by an Action object, which is 1:M with Page.
    """

    TREEMAP_SIZE = (1200, 620)
    USABLE_TAGS = [tag.name for tag in Tag.objects.all()]

    script = models.ForeignKey(Script)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="children")
    url = models.URLField(max_length=2048)

    def __del__(self):
        """
        On garbage collection, kill the webdriver if it exists
        This is easy but kind of precarious so in the future we might want implement it with __enter__ and __exit__ instead
        """

        if hasattr(self, '_webdriver'):
            self._webdriver.quit()

    @property
    def webdriver(self):
        """
        Initializes a webdriver session for this object if one does not already exist
        Navigates the webdriver to the object's url
        """

        if not self.url:
            raise AttributeError('Cannot initialize webdriver: missing url')

        if not hasattr(self, '_webdriver'):
            self._webdriver = webdriver.PhantomJS()
            self._webdriver.get(self.url)
            self._webdriver.maximize_window()

        return self._webdriver

    @property
    def size(self):
        """
        Returns the size of the page as a tuple of (width, height)
        """

        if not hasattr(self, '_size'):
            page_width = self.webdriver.execute_script('return document.getElementsByTagName(\'body\')[0].clientWidth')
            page_height = self.webdriver.execute_script('return document.getElementsByTagName(\'body\')[0].clientHeight')
            self._size = (page_width, page_height)

        return self._size

    @property
    def soup(self):
        """
        Returns a BeautifulSoup representation of the current DOM
        """

        if not hasattr(self, '_soup'):
            self._soup = BeautifulSoup(self.webdriver.page_source)

        return self._soup

    @property
    def tree(self):
        """
        Returns a dict for use with http://bost.ocks.org/mike/treemap/
        """

        def _add_soup_node_to_tree(node):
            """
            Recursively builds the tree dict
            """
            if hasattr(node, 'children'):
                return {'name': node.name, 'children': [_add_soup_node_to_tree(child) for child in node.children if
                                                        (type(child) == bs4_Tag and child.name in self.USABLE_TAGS) or
                                                        (type(child) == NavigableString and child.strip())]}
            else:
                node_contents = unicode(node.strip())
                return {'name': node_contents, 'value': len(node_contents)}

        if not hasattr(self, '_tree'):
            self._tree = {}
            root_node = self.soup.find('html')
            self._tree = _add_soup_node_to_tree(root_node)
        return self._tree


class Action(ExtendedModel):

    """
    This model represents a single atomic action to take on a web page.
    During playback, Actions are traversed in a tree-like structure, so this model is self-referential.
    Possible Action types are limited to a subset of automatable actions supported by the selenium Python bindings.
    """

    page = models.ForeignKey(Page)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="children")
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
