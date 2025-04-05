import os
import yaml

from .defs import DEF_ROOT
from .stream import Stream

_event_registry: dict[str, Stream] = {}


async def initialize(config_file: str) -> None:
    global _event_registry, _root

    with open(config_file, 'r') as f:
        data = yaml.safe_load(f)

        root = data.get('root') if 'root' in data else DEF_ROOT
        os.makedirs(root, exist_ok=True)

        _event_registry = {
            stream: Stream(root, *stream) for stream in data['streams']
        }
