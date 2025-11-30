from http.server import BaseHTTPRequestHandler
from executor.worker import Worker

class Handler(BaseHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
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
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        w = Worker()
        w.start()

        self.wfile.write(b'{"streaming": "Options are ON or OFF"}')

    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>404 Not Found</h1>')