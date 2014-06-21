import pytest
from atmatr.apps.frontend.models import Page, Tag


class TestPage_source:

    @pytest.mark.django_db
    def test_get_correct_source(self, model_mommy):
        """
        Test that the Page.source is indeed the HTML source of the correct page
        """

        page = model_mommy.make('Page', url='http://example.com')
        title_tag = page.source.find('title')
        h1_tag = page.source.find('h1')
        assert title_tag.string == 'Example Domain'
        assert h1_tag.string == 'Example Domain'


class TestPage_segments:

    @pytest.mark.django_db
    def test_segments_are_structured(self, model_mommy):
        """
        Test that all Page.segments root nodes are limited to s_format_root tags
        """
        page = model_mommy.make('Page', url='http://www.iana.org/domains/reserved')
        structure_tags = [model_mommy.make('Tag', name='dl', category='s_format_root'),
                          model_mommy.make('Tag', name='ul', category='s_format_root'),
                          model_mommy.make('Tag', name='ol', category='s_format_root'),
                          model_mommy.make('Tag', name='table', category='s_format_root'),
                          model_mommy.make('Tag', name='form', category='s_format_root'), ]
        segments = page.segments
        root_tags = Tag.objects.filter(category='s_format_root')
        for segment in segments:
            assert segment.name in [root_tag.name for root_tag in root_tags]
