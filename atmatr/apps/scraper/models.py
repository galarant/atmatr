from __future__ import absolute_import
from django.db import models
from atmatr.models import (
    ucModel,
    NamedModel,
    TimestampModel,
    ExtendedModel,
)

# MODELS TO REPRESENT ABSTRACT FUNCTION DEFINITIONS


class DataType(NamedModel):

    """
    This model represents the basic data types that are supported by the application.
    To start we should stick with simple JSON-supported data types and nothing else.
    """

    pass


class ClassDef(ExtendedModel):

    """
    This model represents a class definition in the selenium python package
    http://selenium-python.readthedocs.org/en/latest/
    """

    pass


class FunctionDef(ExtendedModel):

    """
    This model represents a function definition in the selenium python package
    http://selenium-python.readthedocs.org/en/latest/
    """

    klass = models.ForeignKey(ClassDef, null=True)
    is_method = models.NullBooleanField()  # True = class method, False = class attribute, Null = base function
    return_type = models.ForeignKey(ClassDef, null=True, related_name='+')  # helps to chain actions


class ArgDef(ucModel, TimestampModel):

    """
    This model represents a positional argument in a function definition in the selenium python package
    http://selenium-python.readthedocs.org/en/latest/
    """

    function = models.ForeignKey(FunctionDef, related_name="args")
    position = models.SmallIntegerField()
    data_type = models.ForeignKey(DataType)


class KwargDef(ExtendedModel):

    """
    This model represents a keyword argument in a function definition in the selenium python package
    http://selenium-python.readthedocs.org/en/latest/
    """

    function = models.ForeignKey(FunctionDef, related_name="kwargs")
    data_type = models.ForeignKey(DataType)
