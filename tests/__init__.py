from flask import Flask
from flask_jinjahelpers import init_jinja_env


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
