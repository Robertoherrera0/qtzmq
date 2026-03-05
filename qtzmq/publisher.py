import zmq
import json


class QtPublisher:

    def __init__(self, address):

        self.ctx = zmq.Context.instance()

        self.socket = self.ctx.socket(zmq.PUB)
        self.socket.bind(address)

    def send(self, msg):

        if isinstance(msg, dict):
            self.socket.send_json(msg)
        else:
            self.socket.send(msg)

    def close(self):

        self.socket.close(0)