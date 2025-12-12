import time
import redis
from dto.command import CommandRequest
from multiprocessing import Process

database = redis.Redis(host="localhost", port=6379, db=0)
TASK_STATUS_KEY = "RADIO_TASK_STATUS"

class Worker(Process):

    def __init__(self, command_request: CommandRequest):
        super().__init__()

    def run(self):
        self.work()

    def work(self):
        print("MyProcess: running...")
        database.set(TASK_STATUS_KEY, "running")
        
        time.sleep(5.0)
        
        database.set(TASK_STATUS_KEY, "completed")
        print("MyProcess: ended")