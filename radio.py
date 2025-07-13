#!/usr/bin/python3
import sys
import logging
import logger
import executor
from file import CFile
from command import Command


def start():
    log = logger.getLogger("start", logging.INFO)
    log.info("Starting the radio...")

def setup():
    log = logger.getLogger("setup", logging.INFO)
    log.info("Setup the radio env...")

    # Get the commands
    cFileHandler = CFile(log)
    commands = cFileHandler.readCommands()

    # Execute them
    executor.executeCommands(log, commands)

log = logger.getLogger("pre-run", logging.INFO)
call_script_info = "The script should be called with either 'setup' or 'start'."

args = sys.argv
if len(args) != 2:
    log.error("Incorect number of arguments. " + call_script_info)
    exit(1)

match args[1]:
    case "start":
        start()

    case "setup":
        setup()

    case _:
        log.error(call_script_info)
        exit(2)
