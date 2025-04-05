import os
import yaml

from .utils import sync_create_dir 
from .defs import DEF_ROOT
from .stream import StreamInfo


class _Hub:
    event_registry: dict[str, StreamInfo]

    def __init__(self, config_file: str) -> None:
        with open(config_file, 'r') as f:
            data = yaml.safe_load(f)

            root = data.get('root') if 'root' in data else DEF_ROOT
            sync_create_dir(root)            

            self.event_registry = {
                stream['name']: StreamInfo(root, **stream) for stream in data['streams']
            }


__hub_instance: _Hub | None = None

def initalize(config_file: str):
    global __hub_instance
    if not __hub_instance:
        __hub_instance = _Hub(config_file)
