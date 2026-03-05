import zmq
import json
import threading

from ._qt import QObject, Signal


class QtSubscriber(QObject):

    message = Signal(object)
    error = Signal(str)

    def __init__(self, address, topic=""):
        super().__init__()

        self.address = address
        self.topic = topic

        self.ctx = zmq.Context.instance()
        self.socket = None

        self._running = False
        self._thread = None

    def start(self):

        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._recv_loop, daemon=True)
        self._thread.start()

    def stop(self):

        self._running = False

        if self.socket:
            self.socket.close(0)

        if self._thread:
            self._thread.join()

    def _recv_loop(self):

        try:
            self.socket = self.ctx.socket(zmq.SUB)
            self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)
            self.socket.connect(self.address)

            poller = zmq.Poller()
            poller.register(self.socket, zmq.POLLIN)

            while self._running:

                events = dict(poller.poll(100))  # 100 ms timeout

                if self.socket in events:

                    msg = self.socket.recv()

                    try:
                        payload = json.loads(msg)
                    except Exception:
                        payload = msg

                    self.message.emit(payload)

        except Exception as e:

            self.error.emit(str(e))