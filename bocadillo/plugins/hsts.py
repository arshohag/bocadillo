from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from .base import plugin


@plugin(activeif="hsts")
def use_hsts(app):
    """Enable [HSTS].

    [HSTS]: /guides/http/middleware.md#hsts

    # Parameters
    hsts (bool):
        If `True`, HTTP traffic is automatically redirected to HTTPS.
        Defaults to `False`.
    """
    app.add_asgi_middleware(HTTPSRedirectMiddleware)
