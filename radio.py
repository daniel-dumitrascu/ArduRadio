#!/usr/bin/python3
import sys
import logging
import logger
import executor
from file import CFile
from command import Command
from options import Options
from setup_options import SetupOptions

def start():
    log = logger.getLogger("start", logging.INFO)
    log.info("Starting the radio...")

def setup(options : Options):
    log = logger.getLogger("setup", logging.INFO)
    log.info("Setup the radio env...")

    # Get the commands
    cFileHandler = CFile(log)
    commands = cFileHandler.readCommands()

    # Execute them
    executor.executeCommands(log, commands)

spaces = " " * 10
call_script_info = "The script should be called with either 'setup' or 'start'.\nOptions are:\n" + spaces + "-skip <number>: tells at what command should the flow start skipping the commands in front."

args = sys.argv
if len(args) < 2:
    print("Incorect number of arguments. " + call_script_info)
    exit(1)   

match args[1]:
    case "start":
        #options = StartOptions(args)
        #start(options)
        pass

    case "setup":
        options = SetupOptions(args)
        setup(options)

    case _:
        print(call_script_info)
        exit(2)
