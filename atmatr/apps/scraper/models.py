from __future__ import absolute_import
from django.db import models
from atmatr.models import (
    ucModel,
    TimestampModel,
    ExtendedModel,
)

# MODELS TO REPRESENT ABSTRACT FUNCTION DEFINITIONS


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


class ArgDef(ucModel, TimestampModel):

    """
    This model represents a positional argument in a function definition in the selenium python package
    http://selenium-python.readthedocs.org/en/latest/
    """

    JSON_DATA_TYPES = (('object', 'object'),
                       ('array', 'array'),
                       ('string', 'string'),
                       ('int', 'int'),
                       ('float', 'float'),
                       ('boolean', 'boolean'))

    function = models.ForeignKey(FunctionDef, related_name="args")
    position = models.SmallIntegerField()
    data_type = models.CharField(max_length=32, choices=JSON_DATA_TYPES)


class KwargDef(ExtendedModel):

    """
    This model represents a keyword argument in a function definition in the selenium python package
    http://selenium-python.readthedocs.org/en/latest/
    """

    JSON_DATA_TYPES = (('object', 'object'),
                       ('array', 'array'),
                       ('string', 'string'),
                       ('int', 'int'),
                       ('float', 'float'),
                       ('boolean', 'boolean'))

    function = models.ForeignKey(FunctionDef, related_name="kwargs")
    data_type = models.CharField(max_length=32, choices=JSON_DATA_TYPES)
