import os

from ..config import settings, SettingsError


def use_sessions(app):
    """Enable cookie-based signed sessions.

    [SessionMiddleware]: https://www.starlette.io/middleware/#sessionmiddleware

    # Parameters
    sessions (bool or dict):
        if `True`, the secret key is obtained from the `SECRET_KEY` environment
        variable. Otherwise, it must be a dictionary which will be passed
        to Starlette's [SessionMiddleware].
    """
    try:
        from starlette.middleware.sessions import SessionMiddleware
    except ImportError as exc:  # pragma: no cover
        if "itsdangerous" in str(exc):
            raise ImportError(
                "Please install the [sessions] extra to use sessions: "
                "`pip install bocadillo[sessions]`."
            ) from exc
        raise exc from None

    sessions = getattr(settings, "SESSIONS", None)

    if sessions is None:
        return

    if sessions is True:
        sessions = {"secret_key": os.getenv("SECRET_KEY")}

    if not sessions.get("secret_key"):
        raise SettingsError(
            "`SESSIONS` must have a non-empty `secret_key` to use sessions."
        )

    app.add_asgi_middleware(SessionMiddleware, **sessions)
