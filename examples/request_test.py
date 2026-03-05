import sys
import signal

from PySide6.QtWidgets import QApplication
from qtzmq import QtRequester


def on_response(msg):
    print("response:", msg)


def shutdown(*args):
    print("Shutting down...")
    app.quit()


app = QApplication(sys.argv)

signal.signal(signal.SIGINT, shutdown)

req = QtRequester("tcp://localhost:6001")
req.response.connect(on_response)

print("Sending request...")

req.request({"ping": True})

sys.exit(app.exec())