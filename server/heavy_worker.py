from multiprocessing import Process
from utils.transform import json_to_obj
from dto.request import Request
import time
import redis
import logging
import logger

class HeavyWorker(Process):
    def __init__(self):
        super().__init__()
        self.log = logger.getLogger("handler", logging.INFO)
        self.database = redis.Redis(host="localhost", port=6379, db=0)

    def run(self):
        self.work()
        pass

    def work(self):
        while True:
            reqdata = self.database.get("RADIO_PENDING_COMAND")
            if reqdata is not None:
                # Get the time when the request was made
                req = json_to_obj(reqdata, Request)
                req_time = req.req_time
                now = time.time()

                if now - req_time >= 2.0:
                    self.log.info("Start the heavy processing command...")
                    # TODO the removel of the pending command should be done using a LUA script
                    self.database.delete("RADIO_PENDING_COMAND")    
            time.sleep(1)
        