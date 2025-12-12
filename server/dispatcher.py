from multiprocessing import Process
from utils.transform import json_to_obj
from executor.management import WorkerManager
from dto.command import CommandRequest
import time
import redis
import logging
import logger

class Dispatcher(Process):
    def __init__(self):
        super().__init__()
        self.log = logger.getLogger("dispatcher", logging.INFO)
        self.database = redis.Redis(host="localhost", port=6379, db=0)
        self.delete_pending_command = self.database.register_script(self.get_lua_delete_script())
        self.worker_manager = WorkerManager()

    def run(self):
        self.startup_cleanup()
        self.work()
        pass

    def startup_cleanup(self):
        # On startup, clean any pending commands
        self.log.info("Performing startup cleanup")
        self.database.delete("RADIO_PENDING_COMMAND")

    def cycle_cleanup(self):
        task_status = self.database.get("RADIO_TASK_STATUS")
        if task_status is not None:
            status_str = task_status.decode('utf-8')
            if status_str == "completed" or status_str == "failed":
                self.log.info("Cleaning up after finished task")
                self.worker_manager.stop()
                self.database.delete("RADIO_TASK_STATUS")

    def work(self):
        while True:
            self.cycle_cleanup()
            reqid = self.database.hget("RADIO_PENDING_COMMAND", "req_id")
            if reqid is not None:
                # Get the time when the request was made
                req_time = float(self.database.hget("RADIO_PENDING_COMMAND", "req_time"))
                now = time.time()

                if now - req_time >= 2.0:
                    self.log.info(f"Processing request {reqid}")
                    # Process the request...
                    self.process_command()
                    self.delete_pending_command(keys=["RADIO_PENDING_COMMAND"], args=[reqid])

            time.sleep(1)

    def process_command(self):
        # If a worker is already running, stop it
        if self.worker_manager.running() == True:
            self.worker_manager.stop()
        
        reqbody = self.database.hget("RADIO_PENDING_COMMAND", "req_body")
        command_obj, err = json_to_obj(reqbody, CommandRequest)

        if command_obj == None:
            self.log.error(err)
            return
        
        # Start a worker to process the new command
        self.worker_manager.start(command_obj)

    def get_lua_delete_script(self):
        return """
        local key = KEYS[1]
        local expected_id = ARGV[1]

        -- read the ID field from the hash
        local stored_id = redis.call("HGET", key, "req_id")

        -- if no match, do nothing
        if stored_id ~= expected_id then
            return 0
        end

        -- delete the key
        redis.call("DEL", key)
        return 1
        """