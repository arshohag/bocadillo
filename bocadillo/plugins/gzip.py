from starlette.middleware.gzip import GZipMiddleware

from ..config import settings


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
