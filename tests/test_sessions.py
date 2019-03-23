import os

import pytest

from bocadillo import App, view
from bocadillo.settings import Settings, SettingsError, create_settings
from bocadillo.testing import create_client
from bocadillo.utils import override_env


def test_sessions_enabled_no_secret_key():
    settings = create_settings()
    app = App()
    app.configure(settings)


@pytest.fixture(name="get_settings")
def fixture_get_settings():
    def _get():
        settings = Settings(environ=os.environ)
        return create_settings(secret_key=settings("SECRET_KEY"))

    return _get


def test_sessions_enabled_secret_key_empty(get_settings):
    app = App()

    with override_env("SECRET_KEY", ""):
        settings = get_settings()

    with pytest.raises(SettingsError):
        app.configure(settings)


def test_sessions_enabled_secret_key_present(get_settings):
    app = App()

    with override_env("SECRET_KEY", "not-so-secret"):
        settings = get_settings()

    app.configure(settings)

    @app.route("/set")
    @view(methods=["post"])
    async def set_session(req, res):
        req.session["data"] = "something"
        res.text = "Saved"

    @app.route("/")
    async def index(req, res):
        data = req.session["data"]
        res.text = f"Hello {data}"

    client = create_client(app)
    client.post("/set")
    response = client.get("/")
    assert "something" in response.text
    assert "session" in response.cookies
