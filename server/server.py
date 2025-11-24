from server import handler
from http.server import HTTPServer
from logging import log

class Server:
  def __init__(self, log):
    self.log = log
    self.port = 8008

  def start(self):
    self.log.info("Starting the server")
    server_address = ('', self.port)
    httpd = HTTPServer(server_address, handler.Handler)
    self.log.info("Server has started successfully")

    httpd.serve_forever()

    