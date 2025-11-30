import time
from dto.request_command import CommandRequest
from multiprocessing import Process

class Worker(Process):

    def __init__(self, command_request: CommandRequest):
        super().__init__()

    def work(self):
        print("MyProcess: running...")
        
        time.sleep(2.0)
        
        print("MyProcess: ended")

    def run(self):
        self.work()