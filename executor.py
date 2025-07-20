import subprocess
import logging
from typing import Tuple
from command import Command
from options import Options
from option import Option

def executeCommands(log: logging.log, commands: list[Command], opts: Options):
    start = opts.options.get(Option.SKIP.value)
    end = len(commands)
    for i in range(start, end):
        log.info("Executing command: " + commands[i].command)
        success, output, error = __executeCommand__(commands[i].fragments, commands[i].input)
        if success:
            if len(output) > 0:
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