from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from executor.management import WorkerManager
from utils.transform import obj_to_json
import redis
import logging
import logger
import time

database = redis.Redis(host="localhost", port=6379, db=0)

class Handler(BaseHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        self.log = logger.getLogger("handler", logging.INFO)
        self.worker_manager = WorkerManager()
        self.routes = {
                '/streaming': self.streaming
            }
        super().__init__(*args, **kwargs)

    def do_POST(self):
        # Check for exact match
        if self.path in self.routes:
            self.routes[self.path]()
            return
        
        # Check for parameterized routes (e.g., /users/123)
        # if path.startswith('/users/'):
        #     user_id = path.split('/')[-1]
        #     UserController.detail(self, user_id)
        #     return
        
        # 404 Not Found
        self.send_404()

    def streaming(self):
        # Get request as json
        content_length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(content_length)
        json_data = obj_to_json(raw_body)

        if json_data is None:
            self.log.error("Invalid JSON received")
            self.construct_response(HTTPStatus.BAD_REQUEST, b'{"error":"Invalid JSON"}', {'Content-Type': 'application/json'})
            return

        # Write it to Redis as pending command
        database.hset("RADIO_PENDING_COMMAND", mapping={
            "req_id": "abc123",
            "req_time": str(time.time()),
            "req_body": json_data
        })

        # Response
        self.construct_response(HTTPStatus.OK, b'{"streaming": "Options are ON or OFF"}', {'Content-Type': 'application/json'})

        # if self.worker_manager.running() == True:
        #     self.worker_manager.stop() 

        # content_length = int(self.headers.get('Content-Length', 0))
        # raw_body = self.rfile.read(content_length)
        # dto, err_mess = bytes_to_DTO(raw_body)

        # if dto == None:
        #     self.log(err_mess)
        #     return

        # self.worker_manager.start(dto)
        
    def command(self):
        pass

    def send_404(self):
        header = {
            'Content-Type': 'text/html'
        }
        self.construct_response(HTTPStatus.NOT_FOUND, b'<h1>404 Not Found</h1>', header)

    def construct_response(self, status_code, body, headers={}):
        self.send_response(status_code)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)