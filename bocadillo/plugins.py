import os
from typing import Union, Optional

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .config import settings, SettingsError
from .constants import DEFAULT_CORS_CONFIG
from .staticfiles import static


def use_allowed_hosts(app):
    """Restrict which hosts an application is allowed to be served at.

    # Parameters
    allowed_hosts (list of str, optional):
        a list of hosts. If the list contains `"*"`, any host is allowed.
        Defaults to `["*"]`.
    """
    allowed_hosts = getattr(settings, "ALLOWED_HOSTS", None)
    if allowed_hosts is None:
        allowed_hosts = ["*"]

    app.add_asgi_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)


def use_cors(app):
    """Enable CORS (Cross-Origin Resource Sharing) headers.

    [constants.py]: /api/constants.md
    [CORSMiddleware]: https://www.starlette.io/middleware/#corsmiddleware

    # Parameters
    cors (bool or dict):
        If `True`, the default configuration defined in [constants.py] is used.
        Otherwise, the dictionary is passed to Starlette's [CORSMiddleware].
    """
    cors: Optional[Union[bool, dict]] = getattr(settings, "CORS", None)

    if cors is None:
        return

    if cors is True:
        cors = dict(DEFAULT_CORS_CONFIG)

    app.add_asgi_middleware(CORSMiddleware, **cors)


def use_gzip(app):
    """Enable [GZip] compression.

    [GZip]: /guides/http/middleware.md#gzip

    # Parameters
    gzip (bool):
        If `True`, automatically compress responses for clients that support it.
        Defaults to `False`.
    gzip_min_size (int):
        Compress only responses that have more bytes than the specified value.
        Defaults to `1024`.
    """
    if not getattr(settings, "GZIP", False):
        return

    gzip_min_size = getattr(settings, "GZIP_MIN_SIZE", 1024)
    app.add_asgi_middleware(GZipMiddleware, minimum_size=gzip_min_size)


def use_hsts(app):
    """Enable [HSTS].

    [HSTS]: /guides/http/middleware.md#hsts

    # Parameters
    hsts (bool):
        If `True`, HTTP traffic is automatically redirected to HTTPS.
        Defaults to `False`.
    """
    if not getattr(settings, "HSTS", None):
        return

    app.add_asgi_middleware(HTTPSRedirectMiddleware)


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


def use_staticfiles(app):
    """Enable static files serving with WhiteNoise.

    # Parameters
    static_dir (str):
        the name of the directory containing static files, relative to
        the application entry point.
        Set to `None` to not serve any static files.
        Defaults to `"static"`.
    static_root (str):
        the path prefix for static assets. Defaults to `"static"`.
    static_config (dict):
        Extra static files configuration attributes.
        See also #::bocadillo.staticfiles#static.
    """
    static_root = getattr(settings, "STATIC_ROOT", "static")
    static_dir = getattr(settings, "STATIC_DIR", "static")
    static_config = getattr(settings, "STATIC_CONFIG", {})

    if static_dir is None:
        return

    app.mount(static_root, static(static_dir, **static_config))
