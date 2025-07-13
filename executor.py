import subprocess
import logging
from typing import Tuple
from command import Command

def executeCommands(log: logging.log, commands: list[Command]):
    for comm in commands:
        log.info("Executing command: " + comm.command)
        splitCommand = comm.command.split()
        success, output, error = __executeCommand__(splitCommand, comm.input)
        if success:
            log.info(output)
        else:
            log.error(error)
            break

def __executeCommand__(cmd: list, input: str, shell: bool = False) -> Tuple[bool, str, str]:
    try:
        result = subprocess.run(
            cmd,
            input=input,
            capture_output=True,
            text=True,
            shell=shell,
            timeout=30  # Prevent hanging
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)