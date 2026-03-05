import zmq
import json
import threading

from ._qt import QObject, Signal


class QtRequester(QObject):

    response = Signal(object)
    error = Signal(str)

    def __init__(self, address):
        super().__init__()

        self.address = address

        self.ctx = zmq.Context.instance()
        self.socket = None

        self._thread = None

    def request(self, msg):

        if self._thread and self._thread.is_alive():
            return

        self._thread = threading.Thread(
            target=self._request_loop,
            args=(msg,),
            daemon=True,
        )

        self._thread.start()

    def _request_loop(self, msg):

        try:

            self.socket = self.ctx.socket(zmq.REQ)
            self.socket.connect(self.address)

            if isinstance(msg, dict):
                self.socket.send_json(msg)
                reply = self.socket.recv_json()
            else:
                self.socket.send(msg)
                reply = self.socket.recv()

            self.response.emit(reply)

        except Exception as e:

            self.error.emit(str(e))

        finally:

            if self.socket:
                self.socket.close(0)