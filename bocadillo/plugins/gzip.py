from starlette.middleware.gzip import GZipMiddleware

from .base import plugin


@plugin(if_set="GZIP")
def use_gzip(app, gzip_min_size: int = 1024):
    """Enable [GZip] compression.

    [GZip]: /guides/http/middleware.md#gzip

    # Settings
    GZIP (bool):
        If `True`, automatically compress responses for clients that support it.
        Defaults to `False`.
    GZIP_MIN_SIZE (int):
        Compress only responses that have more bytes than the specified value.
        Defaults to `1024`.
    """
    app.add_asgi_middleware(GZipMiddleware, minimum_size=gzip_min_size)
