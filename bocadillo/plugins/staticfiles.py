from typing import Optional


from ..staticfiles import static
from .base import plugin


@plugin()
def use_staticfiles(
    app,
    static_dir: Optional[str] = "static",
    static_root: str = "static",
    static_config: dict = None,
):
    """Enable static files serving with WhiteNoise.

    # Settings
    STATIC_DIR (str):
        the name of the directory containing static files, relative to
        the application entry point.
        Set to `None` to not serve any static files.
        Defaults to `"static"`.
    STATIC_ROOT (str):
        the path prefix for static assets. Defaults to `"static"`.
    STATIC_CONFIG (dict):
        Extra static files configuration attributes.
        See also #::bocadillo.staticfiles#static.
    """
    if static_dir is None:
        return

    if static_config is None:
        static_config = {}

    app.mount(static_root, static(static_dir, **static_config))


@use_staticfiles.revert
def revert(app, static_root, **kwargs):
    app.unmount(static_root)
