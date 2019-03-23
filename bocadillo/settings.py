from typing import Any
from types import SimpleNamespace

from starlette.config import Config as _Settings, environ as _environ

Settings = _Settings
environ = _environ


class SettingsError(Exception):
    """Raised when a setting is missing or has an invalid value."""


def create_settings(**kwargs: Any) -> Any:
    kwargs = {key.upper(): value for key, value in kwargs.items()}
    return SimpleNamespace(**kwargs)
