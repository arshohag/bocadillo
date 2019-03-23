from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware


from .base import Plugin


class HSTSPlugin(Plugin):
    """Enable [HSTS].

    [HSTS]: /guides/http/middleware.md#hsts

    # Settings
    HSTS (bool):
        If `True`, HTTP traffic is automatically redirected to HTTPS.
        Defaults to `False`.
    """

    apply_if_set = "HSTS"

    def apply(self, app):
        app.add_asgi_middleware(HTTPSRedirectMiddleware)
