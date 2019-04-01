from typing import List

from starlette.middleware.trustedhost import TrustedHostMiddleware

from ..config import settings


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
