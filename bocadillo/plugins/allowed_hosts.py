from typing import List

from starlette.middleware.trustedhost import TrustedHostMiddleware

from .base import plugin


@plugin()
def use_allowed_hosts(app, allowed_hosts: List[str] = None):
    """Restrict which hosts an application is allowed to be served at.

    # Settings
    ALLOWED_HOSTS (list of str, optional):
        a list of hosts. If the list contains `"*"`, any host is allowed.
        Defaults to `["*"]`.
    """

    if allowed_hosts is None:
        allowed_hosts = ["*"]

    app.add_asgi_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
