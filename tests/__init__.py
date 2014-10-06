from flask import Flask
from flask_jinjahelpers import init_jinja_env, url_for_current
import pytest


class TemplateHelperTestCase(object):
    def setup_method(self, method):
        class Application(Flask):
            def create_jinja_environment(self):
                rv = super(Application, self).create_jinja_environment()
                return init_jinja_env(rv)

        self.app = Application(__name__)
        self.app.debug = True
        self.setup_views()

        self.client = self.app.test_client()
        self.context = self.app.test_request_context()
        self.context.push()

    def teardown_method(self, method):
        self.context.pop()
        self.context = None
        self.client = None
        self.app = None


@pytest.mark.parametrize(
    ('requested_url', 'expected_url'),
    [
        ('/view1/', '/view1/'),
        ('/view1/?foo=bar', '/view1/?foo=bar'),
        ('/view1/?foo=bar&foo=baz', '/view1/?foo=bar&foo=baz'),
        ('/view2/1', '/view2/1'),
        ('/view2/1?foo=bar', '/view2/1?foo=bar'),
        ('/view2/1?foo=bar&foo=baz', '/view2/1?foo=bar&foo=baz'),
        ('/view3/', '/view3/?foo=baz'),
        ('/view3/?foo=bar', '/view3/?foo=baz')
    ]
)
def test_url_for_current(requested_url, expected_url):
    app = Flask(__name__)
    app.debug = True

    @app.route('/view1/')
    def view1():
        return url_for_current()

    @app.route('/view2/<int:id>')
    def view2(id):
        return url_for_current()

    @app.route('/view3/')
    def view3():
        return url_for_current(foo='baz')

    client = app.test_client()
    response = client.get(requested_url)
    assert response.data == expected_url
