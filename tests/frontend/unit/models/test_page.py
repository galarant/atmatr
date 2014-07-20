import pytest
import json
from atmatr.apps.frontend.models import Page, Tag
from tests.helpers import profile


class TestPage:

    def test_tree_is_well_formed(self):
        """
        Test that the tree formed from the page source is a valid JSON-ifiable dict
        """

        from pprint import pprint
        page = Page(url='http://www.iana.org/domains/reserved')
        json_tree = json.dumps(page.tree)
        pprint(page.tree)
