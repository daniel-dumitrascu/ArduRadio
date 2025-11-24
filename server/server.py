from logging import log

class Server:
  def __init__(self, log):
    self.log = log

  def start(self):
    self.log.info("Starting the server")
    # add server internals here
    self.log.info("Server has started successfully")