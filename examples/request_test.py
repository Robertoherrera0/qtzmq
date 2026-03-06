import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
)

from qtzmq import request, stream

ADDR = "tcp://127.0.0.1:8006"


class Client(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Requester Example")

        layout = QVBoxLayout()

        self.btn = QPushButton("Send Request")
        self.log = QTextEdit()

        layout.addWidget(self.btn)
        layout.addWidget(self.log)

        self.setLayout(layout)

        self.btn.clicked.connect(self.send_request)

        stream("rpc").response.connect(self.handle_response)

    def send_request(self):

        payload = {
            "type": "ping",
            "value": 123
        }

        stream("rpc").request(payload)

    def handle_response(self, payload):

        self.log.append(str(payload))


app = QApplication(sys.argv)

request("rpc", ADDR)

win = Client()
win.show()

sys.exit(app.exec())