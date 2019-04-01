import pytest

from bocadillo import settings
from bocadillo.testing import create_client


def test_basic(raw_app):
    @raw_app.install
    def use_foo(app):
        @app.route("/foo")
        async def foo(req, res):
            res.text = "Foo"

    app = raw_app.configure()
    client = create_client(app)

    r = client.get("/foo")
    assert r.status_code == 200
    assert r.text == "Foo"


def test_use_settings(raw_app):
    @raw_app.install
    def use_hello(app):
        hello_message = getattr(settings, "HELLO_MESSAGE")

        @app.route("/hello")
        async def foo(req, res):
            res.text = hello_message

    app = raw_app.configure(hello_message="Hello, plugins!")
    client = create_client(app)

    r = client.get("/hello")
    assert r.status_code == 200
    assert r.text == "Hello, plugins!"


def test_cannot_reconfigure(app):
    with pytest.raises(RuntimeError) as ctx:
        app.configure()
