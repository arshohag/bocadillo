from typing import Union, Optional

from starlette.middleware.cors import CORSMiddleware

from ..config import settings
from ..constants import DEFAULT_CORS_CONFIG


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
