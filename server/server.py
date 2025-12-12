from server import handler
from http.server import HTTPServer
from logging import log
from server.dispatcher import Dispatcher

class Server:
  def __init__(self, log):
    self.log = log
    self.port = 8008

  def start(self):
    self.log.info(f"Starting the server at port {self.port}")

    # Create the backend heavy worker and start it
    worker = Dispatcher()
    worker.start()

    # Start listening for requests on the main process
    server_address = ('', self.port)
    httpd = HTTPServer(server_address, handler.Handler)
    self.log.info("Server has started successfully")

    httpd.serve_forever()

    