import sys
import json

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
)

from qtzmq import subscribe, stream, stop_all

ADDR = "tcp://127.0.0.1:8000"


class MetadataWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.title = QLabel("Metadata Viewer")
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(self.title)
        layout.addWidget(self.log)

        self.setLayout(layout)

        stream("data").on("metadata", self.handle_metadata)

    def handle_metadata(self, payload):
        data = payload.get("data", {})
        self.log.append(json.dumps(data, indent=2))


class StatusWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.title = QLabel("Status Viewer")
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(self.title)
        layout.addWidget(self.log)

        self.setLayout(layout)

        stream("data").on("status", self.handle_status)

    def handle_status(self, payload):

        self.log.append(str(payload))


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("qtzmq multi-widget example")
        self.resize(900, 500)

        layout = QHBoxLayout()

        self.meta = MetadataWidget()
        self.status = StatusWidget()

        layout.addWidget(self.meta)
        layout.addWidget(self.status)

        self.setLayout(layout)

    def closeEvent(self, event):
        stop_all()
        event.accept()


if __name__ == "__main__":

    subscribe("data", ADDR)

    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec())