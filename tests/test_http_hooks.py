from bocadillo import App, hooks
from .utils import function_hooks, class_hooks


def test_function_hooks(app: App, client):
    with function_hooks() as (before, after):

        @app.route("/foo")
        @hooks.before(before)
        @hooks.after(after)
        async def foo(req, res):
            pass

        client.get("/foo")


def test_pass_extra_args(app: App, client):
    with function_hooks(expected_after=1) as (before, after):

        @app.route("/foo")
        class Foo:
            @hooks.before(before, True)  # positional
            @hooks.after(after, value=1)  # keyword
            async def get(self, req, res):
                pass

        client.get("/foo")


def test_classed_based_hooks(app: App, client):
    with class_hooks() as (before, after):

        @app.route("/foo")
        class Foo:
            @hooks.before(before)
            @hooks.after(after)
            async def get(self, req, res):
                pass

        client.get("/foo")


def test_use_hook_on_view_class(app: App, client):
    with class_hooks() as (before, after):

        @app.route("/foo")
        @hooks.before(before)
        @hooks.after(after)
        class Foo:
            async def get(self, req, res):
                pass

        client.get("/foo")


def test_method_hooks(app: App, client):
    with class_hooks() as (before, after):

        @app.route("/foo")
        class Foo:
            @hooks.before(before)
            @hooks.after(after)
            async def get(self, req, res):
                pass

        client.get("/foo")


def test_before_does_not_run_if_method_not_allowed(app: App, client):
    with function_hooks(False, False) as (before, after):

        @app.route("/foo")
        @hooks.before(before)
        @hooks.after(after)
        class Foo:
            async def get(self, req, res):
                pass

        response = client.put("/foo")
        assert response.status_code == 405
