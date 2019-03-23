import re
import inspect
from typing import Any, Callable, Dict, Optional

PLUGIN_NAME_REGEX = re.compile(r"^use_(.*)$")
REQUIRED = object()
UNDEFINED = object()


def _get_name(func) -> str:
    match = PLUGIN_NAME_REGEX.match(func.__name__)
    if not match:
        raise ValueError(
            f"Cannot infer plugin name from {func}. "
            "Use the 'use_{name}' naming convention "
            "or pass the `name` parameter."
        )
    return match.group(1)


def _get_settings_extractor(func: Callable) -> Callable:
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
                value = getattr(settings, key.upper())
            else:
                value = getattr(settings, key.upper(), default)

            extracted[key] = value

        return extracted

    return extract


class Plugin:
    def __init__(
        self,
        func: Callable,
        name: Optional[str],
        if_set: Optional[str],
        permanent: bool,
    ):
        if name is None:
            name = _get_name(func)

        self.func = func
        self.name = name
        self.if_set = if_set
        self.permanent = permanent
        self._revert = None

        self.extract_settings = _get_settings_extractor(func)
        self.configured_apps = {}

    def should_install(self, settings: Any) -> bool:
        if self.if_set is None:
            return True

        value = getattr(settings, self.if_set, UNDEFINED)
        return value not in (UNDEFINED, False)

    def revert(self, func: Callable) -> Callable:
        self._revert = func
        return func

    def __call__(self, app, settings) -> None:
        if not self.should_install(settings):
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


def plugin(
    name: str = None, if_set: str = None, permanent: bool = False
) -> Callable[[Callable], Plugin]:
    def decorate(func: Callable) -> Plugin:
        return Plugin(func, name=name, if_set=if_set, permanent=permanent)

    return decorate
