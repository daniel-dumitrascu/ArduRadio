from multiprocessing import Process
from utils.transform import json_to_obj
import time
import redis
import logging
import logger

class HeavyWorker(Process):
    def __init__(self):
        super().__init__()
        self.log = logger.getLogger("handler", logging.INFO)
        self.database = redis.Redis(host="localhost", port=6379, db=0)
        self.delete_pending_command = self.database.register_script(self.get_lua_delete_script())

    def run(self):
        self.work()
        pass

    def work(self):
        while True:
            reqid = self.database.hget("RADIO_PENDING_COMMAND", "req_id")
            if reqid is not None:
                # Get the time when the request was made
                req_time = float(self.database.hget("RADIO_PENDING_COMMAND", "req_time"))
                now = time.time()

                if now - req_time >= 2.0:
                    # Process the request...
                    self.delete_pending_command(keys=["RADIO_PENDING_COMMAND"], args=[reqid])

            time.sleep(1)

    def get_lua_delete_script(self):
        return """
        local key = KEYS[1]
        local expected_id = ARGV[1]

        -- read the ID field from the hash
        local stored_id = redis.call("HGET", key, "id")

        -- if no match, do nothing
        if stored_id ~= expected_id then
            return 0
        end

        -- delete the key
        redis.call("DEL", key)
        return 1
        """