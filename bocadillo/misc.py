from typing import Any
from os.path import join, dirname, abspath

_ASSETS_DIR = join(dirname(abspath(__file__)), "assets")


# TODO make async using aiofiles?
def read_asset(filename: str) -> str:
    with open(join(_ASSETS_DIR, filename), "r") as f:
        return f.read()


def get_members(obj: Any) -> dict:
    return {
        key: getattr(obj, key) for key in dir(obj) if not key.startswith("__")
    }
