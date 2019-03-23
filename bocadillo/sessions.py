from typing import TYPE_CHECKING, Any

from .settings import SettingsError

if TYPE_CHECKING:
    from .applications import App


def use_sessions(app: "App", settings: Any):
    """Plugin for cookie-based signed sessions.

    [SessionMiddleware]: https://www.starlette.io/middleware/#sessionmiddleware

    # Settings
    SECRET_KEY (str):
        the secret key to use to sign cookies. Must be set to a non-empty value
        for sessions to be enabled.
    SESSIONS_CONFIG (dict):
        An optional dictionary of sessions configuration parameters.
        See [SessionMiddleware].
    """
    if not hasattr(settings, "SECRET_KEY"):
        return

    try:
        from starlette.middleware.sessions import SessionMiddleware
    except ImportError as exc:  # pragma: no cover
        if "itsdangerous" in str(exc):
            raise ImportError(
                "Please install the [sessions] extra to use sessions: "
                "`pip install bocadillo[sessions]`."
            ) from exc
        raise exc from None

    secret_key: str = getattr(settings, "SECRET_KEY")
    if not secret_key:
        raise SettingsError(
            "A non-empty SECRET_KEY setting must be set to use sessions."
        )

    sessions_config: dict = getattr(settings, "SESSIONS_CONFIG", {})
    sessions_config["secret_key"] = secret_key

    app.add_asgi_middleware(SessionMiddleware, **sessions_config)
