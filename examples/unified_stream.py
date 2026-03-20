import sys
import time
import json
import threading

from PySide6.QtWidgets import QApplication

from qtzmq import subscribe, request, stream, requester 

PUB_ADDR = "tcp://127.0.0.1:7000"
REP_ADDR = "tcp://127.0.0.1:7006"


def backend():

    import zmq

    ctx = zmq.Context()

    pub = ctx.socket(zmq.PUB)
    pub.bind(PUB_ADDR)

    rep = ctx.socket(zmq.REP)
    rep.bind(REP_ADDR)

    time.sleep(1)  # allow subscriber to connect

    while True:
        # PUB message
        pub.send_json({
            "type": "metadata",
            "metadata": {"scan": "test"},
        })

        # REP message
        try:
            if rep.poll(10):
                msg = rep.recv_string()

                if msg == "snapshot":
                    rep.send_json({
                        "type": "metadata",
                        "metadata": {"scan": "snapshot"},
                    })
                else:
                    rep.send_json({"pong": True})
        except Exception:
            pass

        time.sleep(1)


def main():
    # start fake backend
    threading.Thread(target=backend, daemon=True).start()

    app = QApplication(sys.argv)

    # register streams
    subscribe("data", PUB_ADDR)
    request("data", REP_ADDR)

    # handler 
    def handler(payload):
        print("[STREAM RECEIVED]", payload)

    stream("data").on("metadata", handler)

    # trigger snapshot after app starts
    def trigger():
        print("[REQUESTING SNAPSHOT]")
        requester("data").request("snapshot")

    from PySide6.QtCore import QTimer
    QTimer.singleShot(1000, trigger)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()