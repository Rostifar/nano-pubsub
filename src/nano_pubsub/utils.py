
import os
import json

def serialize_event(data: dict) -> str:
    return json.dumps(data)


def deserialize_event(data: str) -> dict: 
    return json.loads(data)


def sync_parent_dir(file: str) -> None:
    parent_dir = os.path.dirname(os.path.abspath(file))
    fd = os.open(parent_dir if parent_dir else '.', os.O_DIRECTORY)
    os.fsync(fd)
    os.close(fd)


def sync_create_empty_file(file: str):
    try:
        fd = os.open(file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        pass 
    else:
        os.fsync(fd)
        os.close(fd)
        sync_parent_dir(file)


def sync_create_dir(dir: str) -> None:
    os.makedirs(dir, exist_ok=True)
    sync_create_dir(dir)


def sync_append_bytes(file: str, payload: bytes) -> None:
    with open(file, "ab", buffering=0) as f:
        f.write(payload)
        os.fsync(f.fileno())


def sync_append_buffered_bytes(file: str, lines: list[bytes], limit: int) -> None:
    chunk = bytearray()
    for line in lines:
        if len(chunk) + len(line) > limit:
            sync_append_bytes(file, chunk)
            chunk = bytearray()
        else:
            chunk.extend(line)
    if chunk:
        sync_append_bytes(file, chunk)


def sync_write_payload(file: str, payload: bytes) -> None:
    with open(file, "w", buffering=0) as f:
        f.write(payload)
        os.fsync(f.fileno())
