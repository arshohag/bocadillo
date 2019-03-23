import re
import inspect
from functools import partial, update_wrapper
from typing import Any, Callable, Dict, Union, Optional

PLUGIN_NAME_REGEX = re.compile(r"^use_(.*)$")
REQUIRED = object()
UNDEFINED = object()


def _get_plugin_name(func) -> str:
    match = PLUGIN_NAME_REGEX.match(func.__name__)
    if not match:
        raise ValueError(
            f"Cannot infer plugin name from {func}. "
            "Hint: use the 'use_{name}' naming convention "
            "or pass the `name` parameter."
        )
    return match.group(1)


def _build_settings_extractor(func: Callable) -> Callable:
    config = {}

    sig = inspect.signature(func)

    for name, param in sig.parameters.items():
        if name in ("self", "app"):
            continue

        if param.kind is inspect.Parameter.VAR_KEYWORD:
            continue

        if param.default is inspect.Parameter.empty:
            config[name] = REQUIRED
        else:
            config[name] = param.default

    def extract(settings: Any) -> dict:
        extracted: Dict[str, Any] = {}

        for key, default in config.items():
            if default is REQUIRED:
                value = settings[key]
            else:
                value = settings.get(key, default)
            extracted[key] = value

        return extracted

    return extract


class Plugin:
    def __init__(
        self,
        func: Callable,
        name: Optional[str],
        activeif: Optional[Union[str, Callable]],
        permanent: bool,
    ):
        name = _get_plugin_name(func) if name is None else name

        if isinstance(activeif, str):
            setting_name = activeif

            def activeif(settings: dict):  # pylint: disable=function-redefined
                return setting_name in settings

        self.func = func
        self.name = name
        self.activeif: Callable = activeif
        self.permanent = permanent
        self._revert = None

        self.extract_settings = _build_settings_extractor(func)
        self.configured_apps = {}

        update_wrapper(self, func)

    def revert(self, func: Callable) -> Callable:
        self._revert = func
        return func

    def __call__(self, app, settings: dict) -> None:
        if self.activeif is not None and not self.activeif(settings):
            return

        if app in self.configured_apps:
            if self.permanent:
                return
            if self._revert is not None:
                settings = self.configured_apps.pop(app)
                self._revert(app, **settings)
            else:
                raise TypeError(
                    f"{self.name} is already configured for app {app}, "
                    "is not permanent and cannot be reconfigured."
                )

        settings: dict = self.extract_settings(settings)
        self.func(app, **settings)
        self.configured_apps[app] = settings

    def __repr__(self):
        return f"<Plugin: {self}>"

    def __str__(self):
        return self.name


def plugin(
    func: Callable = None,
    name: str = None,
    activeif: Union[str, Callable] = None,
    permanent: bool = False,
):
    kwargs = dict(name=name, activeif=activeif, permanent=permanent)
    if func is None:
        return partial(plugin, **kwargs)
    return Plugin(func, **kwargs)
