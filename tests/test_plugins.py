import pytest

from bocadillo import plugin


def test_basic(app, client):
    @app.install
    @plugin
    def use_foo(app):
        @app.route("/foo")
        async def foo(req, res):
            res.text = "Foo"

    app.configure()

    r = client.get("/foo")
    assert r.status_code == 200
    assert r.text == "Foo"


def test_inject_plugin_settings(app, client):
    @app.install
    @plugin
    def use_hello(app, hello_message):
        @app.route("/hello")
        async def foo(req, res):
            res.text = hello_message

    app.configure(hello_message="Hello, plugins!")

    r = client.get("/hello")
    assert r.status_code == 200
    assert r.text == "Hello, plugins!"


def test_cannot_reconfigure_by_default(app):
    @app.install
    @plugin
    def use_hello(app):
        pass

    app.configure()
    with pytest.raises(TypeError) as ctx:
        app.configure()

    error = str(ctx.value)
    assert "hello" in error


def test_permanent_plugin_is_silently_not_reconfigured(app):
    configured = 0

    @app.install
    @plugin(permanent=True)
    def use_hello(app):
        nonlocal configured
        configured += 1

    for _ in range(5):
        app.configure()

    assert configured == 1


@pytest.mark.parametrize(
    "activeif", ("message", lambda settings: "message" in settings)
)
def test_conditional_install(app, activeif):
    configured = False

    @app.install
    @plugin(activeif=activeif)
    def use_hello(app):
        nonlocal configured
        configured = True

    app.configure()
    assert not configured
    app.configure(message="Hello")
    assert configured


def test_name():
    @plugin
    def use_hello():
        pass

    assert use_hello.name == "hello"

    @plugin(name="bye")
    def use_good_bye():
        pass

    assert use_good_bye.name == "bye"
