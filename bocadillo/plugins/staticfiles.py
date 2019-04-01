from ..config import settings
from ..staticfiles import static


def use_staticfiles(app):
    """Enable static files serving with WhiteNoise.

    # Parameters
    static_dir (str):
        the name of the directory containing static files, relative to
        the application entry point.
        Set to `None` to not serve any static files.
        Defaults to `"static"`.
    static_root (str):
        the path prefix for static assets. Defaults to `"static"`.
    static_config (dict):
        Extra static files configuration attributes.
        See also #::bocadillo.staticfiles#static.
    """
    static_root = getattr(settings, "STATIC_ROOT", "static")
    static_dir = getattr(settings, "STATIC_DIR", "static")
    static_config = getattr(settings, "STATIC_CONFIG", {})

    if static_dir is None:
        return

    app.mount(static_root, static(static_dir, **static_config))


# @use_staticfiles.revert
# def revert(app, static_root, **kwargs):
#     app.unmount(static_root)
