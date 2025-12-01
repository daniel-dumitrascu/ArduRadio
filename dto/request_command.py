import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class CommandRequest:
    command: str
    options: Optional[dict] = None


def json_to_DTO(json_body):
    try:
        data = json.loads(json_body.decode('utf-8'))
    except json.JSONDecodeError:
        return None, b'{"error":"Invalid JSON"}'

    try:
        dto = CommandRequest(**data)
    except TypeError as e:
        return None, f'{{"error":"Bad request structure: {str(e)}"}}'
    
    return dto, None