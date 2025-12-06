import json
from dataclasses import dataclass
from enum import Enum


@dataclass
class CommandRequest:
    def __init__(self, command: int):
        self.command = CommandType(command)

class CommandType(Enum):
    STREAM_START = 1
    STREAM_STOP = 2