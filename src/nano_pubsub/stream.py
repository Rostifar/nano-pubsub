import os
import stat

from uuid import uuid4
from dataclasses import dataclass 


def _is_named_pipe(path: str) -> bool:
    try:
        mode = os.stat(path).st_mode
        return stat.S_ISFIFO(mode)
    except FileNotFoundError:
        return False


@dataclass
class Stream:
    root: str
    name: str
    file_identifier: str | None = None
    
    def __post_init__(self) -> None:        
        if self.file_identifier is None:
            self.file_identifier = f"{self.name}-{uuid4()}"

        self.pipe = os.path.join(self.root, self.file_identifier)
        if os.path.exists(self.pipe) and not _is_named_pipe(self.pipe):
            raise ValueError(f"Invalid stream: file ({self.file}) is not a named pipe.")
        else:
            os.mkfifo(self.pipe)
