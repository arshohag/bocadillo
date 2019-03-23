from ..settings import SettingsError

from .base import Plugin


class SessionsPlugin(Plugin):
    """Enable cookie-based signed sessions.

    [SessionMiddleware]: https://www.starlette.io/middleware/#sessionmiddleware

    # Settings
    SESSIONS (bool or dict):
        if `True`, the secret key is obtained from the `SECRET_KEY` environment
        variable. Otherwise, it must be a dictionary which will be passed
        to Starlette's [SessionMiddleware].
    """

    apply_if_set = "SESSIONS"

    def apply(self, app, sessions: dict):
        try:
            from starlette.middleware.sessions import SessionMiddleware
        except ImportError as exc:  # pragma: no cover
            if "itsdangerous" in str(exc):
                raise ImportError(
                    "Please install the [sessions] extra to use sessions: "
                    "`pip install bocadillo[sessions]`."
                ) from exc
            raise exc from None

        if not sessions.get("secret_key"):
            raise SettingsError(
                "A non-empty `secret_key` must be set to use sessions."
            )

        app.add_asgi_middleware(SessionMiddleware, **sessions)
