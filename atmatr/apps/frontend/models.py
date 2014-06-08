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

# APPLICATION MODELS


class PageTree(ExtendedModel):

    """
    This model represents the tree of pages to traverse during playback.
    Each page in the tree is represented by an ActionTree object, which is 1:M with PageTree.
    """

    user = models.ForeignKey(User, related_name="page_trees")
    period = models.FloatField()  # Amount of time between successive playbacks, in seconds


class ActionTree(ExtendedModel):

    """
    This model represents a tree of actions to take on a single web page.
    During playback, pages themselves are traversed in a tree-like structure, so this model is self-referential.
    Each action in the ActionTree is represented by an Action object, which is 1:M with ActionTree.
    """

    page_tree = models.ForeignKey(PageTree, related_name="action_trees")
    previous_page = models.ForeignKey('self', null=True, blank=True, related_name="next_pages")
    url = models.URLField(max_length=2048)


class Action(ExtendedModel):

    """
    This model represents a single atomic action to take on a web page.
    During playback, Actions are traversed in a tree-like structure, so this model is self-referential.
    Possible Action types are limited to a subset of automatable actions supported by the selenium Python bindings.
    """

    action_tree = models.ForeignKey(ActionTree, related_name="actions")
    previous_action = models.ForeignKey('self', null=True, blank=True, related_name="next_actions")
    function = models.ForeignKey(FunctionDef)


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
