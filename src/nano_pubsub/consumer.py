import os
import json
import asyncio

from typing import Callable
from datetime import datetime
from dataclasses import dataclass

from .hooks import __hub_instance
from .stream import JsonEvent
from .utils import sync_write_payload

COMMIT_INTERVAL_SEC = 60

@dataclass
class Offset:
    committed_at: datetime
    lineno: int

    def serialize(self) -> str:
        return json.dumps(
            dict(
                committed_at=self.committed_at.timestamp(),
                lineno=self.lineno
            ),
        )


    @classmethod
    def deserialize(cls, data: str) -> "Offset":
        data = json.loads(data)
        return cls(
            committed_at=datetime.fromtimestamp(data["committed_at"]),
            lineno=data["lineno"]
        )


@dataclass
class Consumer:
    stream_name: str
    group: str
    
    def __post_init__(self) -> None:
        self._stream = __hub_instance.event_registry[self.stream_name]

        self.offset_file = os.path.join(self._stream.root, self.stream_name, self.group)
        if os.path.exists(self.offset_file):
            self.offset = self._get_last_committed_offset()
        else:
            self.offset = None
        
        self._offset_commit_task = asyncio.create_task(self._commit_offsets())
        self._shutdown = False


    async def _commit_offsets(self):
        while not self._shutdown:
            await asyncio.sleep(COMMIT_INTERVAL_SEC)
            await self.flush()
    
    
    async def _commit_offsets(self) -> None:
        if not self.offset:
            return
        
        payload = self.offset.serialize().encode("utf-8")
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sync_write_payload, payload)


    def _get_last_committed_offset(self):
        with open(self.offset_file, "r") as f:
            line = f.readline().strip()
        return Offset.deserialize(line)


    async def listen(self, on_event: Callable[[JsonEvent], None]) -> None:
        with open(self._stream.log_file) as f:
            f.seek(0)
            if self.offset:
                for _ in range(self.offset.lineno - 1):
                    f.readline()
                
            for line in f.readlines():
                try:
                    on_event(JsonEvent.deserialize(line.strip()))
                except Exception as e:
                    print(f'`on_event` callback failed with exception: {e}.')
            asyncio.sleep(0.1)
