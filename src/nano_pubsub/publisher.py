from typing import Callable
from dataclasses import dataclass

from .main import _event_registry
from .utils import serialize_event

@dataclass
class Publisher:
    stream_name: str
    
    def __post_init__(self) -> None:
        self._stream = _event_registry[self.stream_name]

    def publish_event(self, event: dict) -> None:
        with open(self._stream.pipe, 'w') as pipe:
            pipe.write(serialize_event(event) + "\n")
            pipe.flush()
