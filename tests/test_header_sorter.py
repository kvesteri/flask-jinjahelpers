from flask import render_template_string, url_for, request
from flask_jinjahelpers import header_sort_url
from tests import TemplateHelperTestCase


class TestHeaderSorter(TemplateHelperTestCase):
    def setup_views(self):
        @self.app.route('/')
        def index():
            sorted_fields = request.args.getlist('sort')
            return render_template_string(
                """
                {% from "_tablehelpers.html" import render_header_link %}
                {{
                render_header_link('name', 'Name', sorted_fields)
                }}
                """,
                sorted_fields=sorted_fields
            )

    def test_sort_by_empty_string(self):
        assert header_sort_url('') == (
            '/'
        )

    def test_with_consecutive_calls(self):
        assert header_sort_url('age') == (
            '/?sort=age'
        )
        assert header_sort_url('name') == (
            '/?sort=name'
        )

    def test_with_empty_string_in_sorted_fields(self):
        assert header_sort_url('name', ['']) == (
            '/?sort=name'
        )

    def test_with_hyphen_in_sorted_fields(self):
        assert header_sort_url('name', ['-']) == (
            '/?sort=name'
        )

    def test_sorted_fields_supports_string_as_parameter(self):
        assert header_sort_url('age', 'age') == (
            '/?sort=-age'
        )

    def test_sort_by_single_header(self):
        assert header_sort_url('age', ['name'], max_sorted_fields=2) == (
            '/?sort=age&sort=name'
        )
        assert header_sort_url('name') == '/?sort=name'
        assert header_sort_url('name', ['-name']) == '/?sort=name'
        assert header_sort_url('name', ['name']) == '/?sort=-name'

    def test_with_multiple_sorted_fields(self):
        assert header_sort_url(
            'name', ['name', 'age'], max_sorted_fields=2
        ) == (
            '/?sort=-name&sort=age'
        )

        assert header_sort_url(
            'age', ['name', 'age'], max_sorted_fields=2
        ) == (
            '/?sort=-age&sort=name'
        )

        assert header_sort_url(
            'age', ['name', '-age'], max_sorted_fields=2
        ) == (
            '/?sort=age&sort=name'
        )

        assert header_sort_url(
            'age', ['-age', 'name'], max_sorted_fields=2
        ) == (
            '/?sort=age&sort=name'
        )

    def test_max_number_of_sorted_fields(self):
        assert header_sort_url(
            'name', ['name', 'age'], max_sorted_fields=1
        ) == (
            '/?sort=-name'
        )

    def test_render_header_link(self):
        response = self.client.get(url_for('.index', sort=['name']))

        assert  '<th class="table-sort-asc">' in response.data
        assert '<a href="/?sort=-name">Name</a>' in response.data
        assert '</th>' in response.data

        response = self.client.get(url_for('.index', sort=['-name']))
        assert  '<th class="table-sort-desc">' in response.data
        assert '<a href="/?sort=name">Name</a>' in response.data
        assert '</th>' in response.data

        response = self.client.get(url_for('.index', sort=['name', 'age']))
        assert response.data.count('</th>') == 1
