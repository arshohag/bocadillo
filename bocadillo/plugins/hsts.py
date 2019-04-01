from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from ..config import settings


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
