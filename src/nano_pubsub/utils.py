import json

def serialize_event(data: dict) -> str:
    return json.dumps(data)


def deserialize_event(data: str) -> dict: 
    return json.loads(data)
