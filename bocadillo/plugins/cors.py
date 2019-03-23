from typing import Union

from starlette.middleware.cors import CORSMiddleware

from ..constants import DEFAULT_CORS_CONFIG
from .base import Plugin


class CORSPlugin(Plugin):
    """Enable CORS (Cross-Origin Resource Sharing) headers.

    [constants.py]: /api/constants.md
    [CORSMiddleware]: https://www.starlette.io/middleware/#corsmiddleware

    # Settings
    CORS (bool or dict):
        If `True`, the default configuration defined in [constants.py] is used.
        Otherwise, the dictionary is passed to Starlette's [CORSMiddleware].
    """

    apply_if_set = "CORS"

    def apply(self, app, cors: Union[bool, dict]):
        if cors is True:
            config = DEFAULT_CORS_CONFIG
        else:
            config = {**DEFAULT_CORS_CONFIG, **cors}

        app.add_asgi_middleware(CORSMiddleware, **config)
