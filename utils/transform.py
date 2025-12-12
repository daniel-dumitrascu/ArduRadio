import json
from dataclasses import is_dataclass, asdict


def obj_to_json(obj):
    def default(o):
        # If it's a dataclass, convert to dict
        if is_dataclass(o):
            return asdict(o)
        # If it has a __dict__, use that
        if hasattr(o, "__dict__"):
            return o.__dict__
        # Fallback: convert to string
        return str(o)

    return json.dumps(obj, default=default).encode('utf-8')


def json_to_obj(json_str, cls):
    try:
        data = json.loads(json_str.decode('utf-8'))
        return cls(**data), None
    except json.JSONDecodeError:
        return None, b'{"error":"Invalid JSON"}'
    except TypeError as e:
        return None, f'{{"error":"Bad request structure: {str(e)}"}}'