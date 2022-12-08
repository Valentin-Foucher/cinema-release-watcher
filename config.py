from typing import Any

from frozendict import frozendict
from pyaml_env import parse_config


def load_config(config_file: str = 'config.yaml') -> dict[str, Any]:
    return parse_config(config_file)


def get(path: str):
    v = _config
    for p in path.split('.'):
        if p not in v:
            return None
        v = v.get(p)

    if isinstance(v, dict):
        v = frozendict(v)
    elif isinstance(v, list):
        v = tuple(v)

    return v


_config = load_config()
