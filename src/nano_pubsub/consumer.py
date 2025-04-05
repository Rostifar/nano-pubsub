import asyncio

from typing import Callable
from dataclasses import dataclass

from .hooks import _event_registry
from .utils import deserialize_event

@dataclass
class Consumer:
    stream_name: str
    
    def __post_init__(self) -> None:
        self._stream = _event_registry[self.stream_name]

    async def listen(self, on_event: Callable[[dict], None]) -> None:
        while True:
            with open(self._stream.pipe) as fifo:
                for line in fifo:
                    try:
                        on_event(deserialize_event(line))
                    except Exception as e:
                        print(f'`on_event` callback failed with exception: {e}.')
            asyncio.sleep(0.1)
