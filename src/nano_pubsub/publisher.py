import asyncio

from dataclasses import dataclass

from .stream import JsonEvent
from .hooks import __hub_instance
from .utils import sync_append_buffered_bytes

# N.B. larger events are skipped to ensure concurrent atomic writes.
MAX_BUFFER_SIZE_BYTES = 2048
FLUSH_INTERVAL_SEC = 1.0
FLUSH_BUFFER_THRESHOLD = 32


@dataclass
class Publisher:
    stream_name: str
    
    def __post_init__(self) -> None:
        self._stream = __hub_instance.event_registry[self.stream_name]
        self._shutdown = False
        self._flush_task = asyncio.create_task(self._periodic_flush())
        self._buffer = []


    async def _periodic_flush(self) -> None:
        while not self._shutdown:
            await asyncio.sleep(FLUSH_INTERVAL_SEC)
            await self.flush()


    def publish_event(self, event: JsonEvent) -> None:
        with open(self._stream.pipe, 'a') as pipe:
            payload = (event.serialize() + "\n").encode("utf-8")
            self._buffer.append(payload)
            
            if len(self._buffer) > FLUSH_BUFFER_THRESHOLD: 
                asyncio.create_task(self.flush())


    async def flush(self) -> None:
        if not self._buffer:
            return
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sync_append_buffered_bytes)

    async def shutdown(self):
        if self._shutdown:
            return 
        self._shutdown = True

        await self.flush()
        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass
