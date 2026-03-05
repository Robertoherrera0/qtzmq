import sys
import signal

from PySide6.QtWidgets import QApplication
from qtzmq import QtSubscriber


def handler(msg):
    print("received:", msg)


def shutdown(*args):
    print("Shutting down...")
    sub.stop()
    app.quit()


app = QApplication(sys.argv)

# allow ctrl+c to end the test
signal.signal(signal.SIGINT, shutdown)

print("Subscriber starting...")

sub = QtSubscriber("tcp://localhost:6000")
sub.message.connect(handler)

sub.start()

sys.exit(app.exec())