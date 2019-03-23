import re
import inspect
from typing import Any, Callable, Dict, NamedTuple, Optional

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

    __base__ = True

    def __init__(
        self, func: Callable, name: Optional[str], if_set: Optional[str]
    ):
        if name is None:
            name = _get_name(func)

        self.func = func
        self.name = name
        self.if_set = if_set
        self.extract_settings = _get_settings_extractor(func)
        self.configured_apps = set()

    def should_apply(self, settings: Any) -> bool:
        if self.if_set is None:
            return True

        value = getattr(settings, self.if_set, UNDEFINED)
        return value not in (UNDEFINED, False)

    def __call__(self, app, settings) -> None:
        if app in self.configured_apps:
            return

        if not self.should_apply(settings):
            return

        settings: dict = self.extract_settings(settings)
        self.func(app, **settings)
        self.configured_apps.add(app)


def plugin(name: str = None, if_set: str = None) -> Plugin:
    def decorate(func):
        return Plugin(func, name=name, if_set=if_set)

    return decorate
