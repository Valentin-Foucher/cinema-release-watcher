from typing import Any


def wrap(obj: Any) -> list[Any]:
    return obj if isinstance(obj, list) else [obj]
