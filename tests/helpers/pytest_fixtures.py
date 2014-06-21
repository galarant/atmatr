import pytest


@pytest.fixture
def json():
    import json
    return json


@pytest.fixture
def mock():
    import mock
    return mock

# TODO: cannot import vcrpy
"""
@pytest.fixture
def vcr():
    from . import vcr
    return vcr
"""


@pytest.fixture
def model_mommy():
    from model_mommy import mommy
    return mommy
