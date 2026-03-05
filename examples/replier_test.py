import sys
import signal

from PySide6.QtWidgets import QApplication
from qtzmq import QtReplier


def on_request(msg):
    print("received request:", msg)

    response = {"reply": "pong"}

    rep.reply(response)


def shutdown(*args):
    print("Shutting down...")
    rep.stop()
    app.quit()


app = QApplication(sys.argv)

signal.signal(signal.SIGINT, shutdown)

rep = QtReplier("tcp://*:6001")
rep.request.connect(on_request)

rep.start()

print("Replier running...")

sys.exit(app.exec())