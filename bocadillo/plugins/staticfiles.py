from typing import Optional


from ..staticfiles import static
from .base import Plugin, Ref


class StaticFilesPlugin(Plugin):
    """Enable static files serving with WhiteNoise.

    # Settings
    STATIC_DIR (str):
        the name of the directory containing static files, relative to
        the application entry point.
        Set to `None` to not serve any static files.
        Defaults to `"static"`.
    STATIC_ROOT (str):
        the path prefix for static assets.
        The value given to `static_dir` is used by default.
    STATIC_CONFIG (dict):
        Extra static files configuration attributes.
        See also #::bocadillo.staticfiles#static.
    """

    def apply(
        self,
        app,
        static_dir: Optional[str] = "static",
        static_root: str = Ref("static_dir"),
        static_config: dict = None,
    ):
        if static_dir is None:
            return

        if static_config is None:
            static_config = {}

        app.mount(static_root, static(static_dir, **static_config))
