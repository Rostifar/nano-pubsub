import os
import json

from datetime import datetime
from dataclasses import dataclass
from .utils import sync_create_empty_file

@dataclass
class StreamInfo:
    root: str 
    name: str 

    def __post_init__(self, root: str, name: str) -> None:
        self.log_file = os.path.join(root, name)
        
        if not os.path.exists(self.log_file):
            sync_create_empty_file(self.log_file)


@dataclass
class JsonEvent:
    data: dict
    timestamp: datetime | None = None

    def serialize(self) -> str:
        now = datetime.now().timestamp()
        model = self.data | dict(
            timestamp = self.timestamp.timestamp() if self.timestamp else now
        )
        return json.dumps(model)

    @classmethod
    def deserialize(cls, data: str) -> "JsonEvent":
        model = json.loads(data)
        timestamp = model.pop('timestamp')
        return cls(
            timestamp=datetime.fromtimestamp(timestamp),
            data=model
        )
