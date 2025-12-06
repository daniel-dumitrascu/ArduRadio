import time
from dto.command import CommandRequest
from multiprocessing import Process

class Worker(Process):

    def __init__(self, command_request: CommandRequest):
        super().__init__()

    def run(self):
        self.work()

    def work(self):
        print("MyProcess: running...")
        
        time.sleep(5.0)
        
        print("MyProcess: ended")