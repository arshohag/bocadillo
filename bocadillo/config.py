from typing import Any, Optional


class SettingsError(Exception):
    """Raised when a setting is missing or has an invalid value."""


class Settings:
    def __init__(self, obj: Optional[Any]):
        for setting in dir(obj):
            if not setting.isupper():
                continue
            value = getattr(obj, setting)
            setattr(self, setting, value)


class LazySettings:
    """A lazy proxy for application settings.

    Once configured, an instance of this class can be used to access settings
    from anywhere in the application code base.
    """

    def __init__(self):
        self._wrapped = None

    def configure(self, obj: Any = None, **options):
        if self.configured:
            raise RuntimeError("Settings are already configured")

        wrapped = Settings(obj)

        for name, option in options.items():
            if name.startswith("_"):
                continue

            if not name.isupper():
                raise SettingsError(f"Setting {name} must be uppercase.")

            setattr(wrapped, name, option)

        self._wrapped = wrapped

    @property
    def configured(self) -> bool:
        return self._wrapped is not None

    def __getattr__(self, name: str) -> Any:
        if not self.configured:
            raise SettingsError(
                f"Requested setting {name} but settings aren't configured yet."
            )

        value = getattr(self._wrapped, name)

        self.__dict__[name] = value  # cache setting

        return value

    def __setattr__(self, name: str, value: Any):
        if name == "_wrapped":
            self.__dict__.clear()
        else:
            self.__dict__.pop(name, None)  # remove from cache
        super().__setattr__(name, value)


settings = LazySettings()  # pylint: disable=invalid-name
