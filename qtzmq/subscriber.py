import zmq
import json
import threading

from collections import defaultdict
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

        self._handlers = defaultdict(list)

        # dispatch handlers from Qt thread
        self.message.connect(self._dispatch)

    def on(self, msg_type, handler):
        self._handlers[msg_type].append(handler)

    def start(self):

        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._recv_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

        if self._thread:
            self._thread.join()

        if self.socket:
            self.socket.close(0)

    def _recv_loop(self):
        try:

            self.socket = self.ctx.socket(zmq.SUB)
            self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)
            self.socket.connect(self.address)

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

                    # emit signal across threads
                    self.message.emit(payload)

        except Exception as e:

            self.error.emit(str(e))

    def _dispatch(self, payload):
        if isinstance(payload, dict):

            msg_type = payload.get("type")

            if msg_type in self._handlers:

                for handler in self._handlers[msg_type]:
                    handler(payload)