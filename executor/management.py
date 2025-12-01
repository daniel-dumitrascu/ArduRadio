import redis
import psutil
import logging
import logger
from dto.request_command import CommandRequest
from executor.worker import Worker

database = redis.Redis(host="localhost", port=6379, db=0)
WORKER_KEY = "RADIO_WORKER"

class WorkerManager():
    def __init__(self):
        self.log = logger.getLogger("worker management", logging.INFO)

    def running(self):
        return True if database.get(WORKER_KEY) is not None else False

    def start(self, command_request: CommandRequest):
        curr_pid = database.get(WORKER_KEY)
        if curr_pid is not None:
            self.log.info("A command is currently executed. please stop it before starting a new one.")
            return
        
        worker = Worker(command_request)
        worker.start()
        database.set(WORKER_KEY, worker.pid)

    def stop(self):
        prev_process = database.get(WORKER_KEY)
        if prev_process:
            database.delete(WORKER_KEY)
            self.kill_process(int(prev_process))

    def kill_process(self, pid):
        try:
            p = psutil.Process(pid)
            self.log.info(f"Killing previous worker (PID={pid})")
            p.terminate()   # send SIGTERM
            p.wait(timeout=3)
        except psutil.NoSuchProcess:
            pass
        except psutil.TimeoutExpired:
            self.log.warning("Process did not exit, sending SIGKILL")
            p.kill()