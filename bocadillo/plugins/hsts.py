from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from .base import plugin


@plugin(if_set="HSTS")
def use_hsts(app):
    """Enable [HSTS].

    [HSTS]: /guides/http/middleware.md#hsts

    # Settings
    HSTS (bool):
        If `True`, HTTP traffic is automatically redirected to HTTPS.
        Defaults to `False`.
    """
    app.add_asgi_middleware(HTTPSRedirectMiddleware)
