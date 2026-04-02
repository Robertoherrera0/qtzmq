# tests/test_requester.py
import sys
import json
import threading
import zmq

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from qtzmq.requester import QtRequester

ADDR = "tcp://127.0.0.1:15555"

def run_rep_server():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.REP)
    sock.bind(ADDR)
    msg = sock.recv_string()
    print(f"[SERVER] received: {msg!r}")
    sock.send_string(json.dumps({"type": "snapshot", "status": "idle", "value": 42}))
    sock.close()
    ctx.term()

def main():
    app = QApplication(sys.argv)

    # start REP server in background
    t = threading.Thread(target=run_rep_server, daemon=True)
    t.start()

    req = QtRequester(ADDR)

    def on_response(resp):
        print(f"[CLIENT] response: {resp}")
        assert isinstance(resp, dict), f"expected dict, got {type(resp)}"
        assert resp.get("type") == "snapshot"
        assert resp.get("value") == 42
        print("[PASS] string request -> dict response works correctly")
        app.quit()

    def on_error(e):
        print(f"[FAIL] error: {e}")
        app.quit()

    req.response.connect(on_response)
    req.error.connect(on_error)

    QTimer.singleShot(100, lambda: req.request("snapshot"))
    QTimer.singleShot(5000, lambda: (print("[FAIL] timeout"), app.quit()))

    sys.exit(app.exec())

if __name__ == "__main__":
    main()