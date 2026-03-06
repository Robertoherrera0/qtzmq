import sys

from PySide6.QtCore import QCoreApplication

from qtzmq import reply, stream

ADDR = "tcp://127.0.0.1:8006"


def handle_request(payload):

    print("received:", payload)

    response = {
        "status": "ok",
        "echo": payload
    }

    stream("rpc").reply(response)


app = QCoreApplication(sys.argv)

reply("rpc", ADDR)

stream("rpc").request.connect(handle_request)

print("Replier running on", ADDR)

sys.exit(app.exec())