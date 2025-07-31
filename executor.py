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
        success, output, error = execute(commands[i].fragments, commands[i].input, 
                                         commands[i].interactive, commands[i].setShell, 
                                         commands[i].timeout)
        if success:
            if len(output) > 0:
                log.info(output)
        else:
            err = error
            if len(output) > 0:
                err = output + err
            log.error(err)
            
            break

def execute(fragments: list[str], input: str, interactive: bool, shell: bool, timeout: int):
    if interactive:
        return __executeInteractiveCommand__(fragments, input)
    else:
        return __executeNonInteractiveCommand__(fragments, input, timeout, shell)


def __executeNonInteractiveCommand__(cmd: list, input: str, timeout: int, shell: bool = False) -> Tuple[bool, str, str]:
    try:
        result = subprocess.run(
            cmd,
            input=input,
            capture_output=True,
            text=True,
            shell=shell,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)
    
def __executeInteractiveCommand__(cmd: list, inputs: list[str]):
    process = subprocess.Popen(
        args=cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Send all inputs
    for input in inputs:
        process.stdin.write(input + '\n')

    stdout, stderr = process.communicate()
    return process.returncode == 0, stdout, stderr