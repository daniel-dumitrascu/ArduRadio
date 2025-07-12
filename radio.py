#!/usr/bin/python3
import sys
import logging

def start():
    log = getLogger("start", logging.INFO)
    log.info("Starting the radio...")

def setup():
    log = getLogger("setup", logging.INFO)
    log.info("Setup the radio...")

def getLogger(log_name, lvl):
    log = logging.getLogger(log_name)
    log.setLevel(lvl)

    # Prevent adding multiple handlers if logger already exists
    if log.handlers:
        return log

    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(lvl)
    console_handler.setFormatter(console_formatter)
    log.addHandler(console_handler)
    return log

log = getLogger("pre-run", logging.INFO)
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


# parse the arguments and select either setup or start
#print("Hello my secret LOVE, python!")
