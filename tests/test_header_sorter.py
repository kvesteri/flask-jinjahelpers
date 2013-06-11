from flask import Flask, render_template_string, url_for, request
from flask_jinjahelpers import header_sort_url, init_jinja_env


class TestHeaderSorter(object):
    def setup_method(self, method):
        class Application(Flask):
            def create_jinja_environment(self):
                rv = super(Application, self).create_jinja_environment()
                return init_jinja_env(rv)

        self.app = Application(__name__)
        self.app.debug = True

        @self.app.route('/')
        def index():
            sorted_fields = request.args.getlist('sort')
            return render_template_string(
                """
                {% from "_tablehelpers.html" import render_header_link %}
                {{
                render_header_link('.index', 'name', 'Name', sorted_fields)
                }}
                """,
                sorted_fields=sorted_fields
            )

        self.client = self.app.test_client()
        self.context = self.app.test_request_context()
        self.context.push()

    def teardown_method(self, method):
        self.context.pop()
        self.context = None
        self.client = None
        self.app = None

    def test_sort_by_header(self):

        assert header_sort_url('.index', 'age', ['name']) == (
            '/?sort=age&sort=name'
        )
        assert header_sort_url('.index', 'name') == '/?sort=name'
        assert header_sort_url('.index', 'name', ['-name']) == '/?sort=name'
        assert header_sort_url('.index', 'name', ['name']) == '/?sort=-name'

        assert header_sort_url('.index', 'name', ['name', 'age']) == (
            '/?sort=-name&sort=age'
        )

        assert header_sort_url('.index', 'age', ['name', 'age']) == (
            '/?sort=-age&sort=name'
        )

        assert header_sort_url('.index', 'age', ['name', 'age']) == (
            '/?sort=-age&sort=name'
        )

        assert header_sort_url('.index', 'age', ['-age', 'name']) == (
            '/?sort=age&sort=name'
        )

    def test_render_template(self):
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
