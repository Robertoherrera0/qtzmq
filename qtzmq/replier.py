import zmq
import json
import threading

from ._qt import QObject, Signal


class QtReplier(QObject):

    request = Signal(object)
    error = Signal(str)

    def __init__(self, address):
        super().__init__()

        self.address = address

        self.ctx = zmq.Context.instance()
        self.socket = None

        self._running = False
        self._thread = None

    def start(self):

        if self._running:
            return

        self._running = True

        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

        if self._thread:
            self._thread.join()

        if self.socket:
            self.socket.close(0)

    def reply(self, msg):

        if isinstance(msg, dict):
            self.socket.send_json(msg)
        else:
            self.socket.send(msg)

    def _loop(self):

        try:

            self.socket = self.ctx.socket(zmq.REP)
            self.socket.bind(self.address)

            poller = zmq.Poller()
            poller.register(self.socket, zmq.POLLIN)

            while self._running:

                events = dict(poller.poll(100))

                if self.socket in events:

                    msg = self.socket.recv()

                    try:
                        payload = json.loads(msg)
                    except Exception:
                        payload = msg

                    self.request.emit(payload)

        except Exception as e:

            self.error.emit(str(e))