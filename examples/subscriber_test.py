import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit

from qtzmq import subscribe, stream

ADDR = "tcp://127.0.0.1:8000"


class Viewer(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(self.log)
        self.setLayout(layout)

        stream("data").on("data", self.handle_data)

    def handle_data(self, payload):
        self.log.append(str(payload))


app = QApplication(sys.argv)

# This creates the subscriber and starts it
subscribe("data", ADDR)

win = Viewer()
win.show()

sys.exit(app.exec())