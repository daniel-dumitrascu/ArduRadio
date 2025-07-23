import json
from logging import log
from pathlib import Path
from command import Command

class CFile:
    def __init__(self, log):
        self.log = log

    def readCommands(self) -> list[Command]:
        filename = "commands.json"
        commands = []

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read().strip()

                if not content:
                    self.log.error("Commands file is empty.")
                    return commands
                
                data = None
                try:
                    data = json.loads(content)
                except json.JSONDecodeError as e:
                    self.log.error(f"Invalid JSON format: {e}")
                    self.log.error(f"Error at line {e.lineno}, column {e.colno}")
                    return []

                if isinstance(data, dict) and "commands" in data:
                    commandsData = data["commands"]
                    if not isinstance(commands, list):
                        self.log.error("The 'commands' property is not a list.")
                        return []
                else:
                    self.log.error("Cannot parse commands file.")
                    return [] 

                for comm_num, entry in enumerate(commandsData, 1):
                    comm = entry["command"]
                    input = entry["input"]
                    interactive = entry["interactive"]
                    description = entry["description"]
                    comm = comm.strip()
                    input = input.strip()

                    if not comm:  # Skip empty lines
                        continue

                    commands.append(Command(comm, input, interactive, description))
        except FileNotFoundError:
            self.log.error(f"Commands file was not found.")
        except UnicodeDecodeError:
            self.log.error(f"Unable to decode '{filename}' as UTF-8. Check file encoding.")
        except Exception as e:
            self.log.error(f"Unexpected error reading commands file: {e}")

        return commands