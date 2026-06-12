# tests/test_requester_curve.py
import sys
import json
import threading
import zmq
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from qtzmq.requester import QtRequester

ADDR = "tcp://127.0.0.1:15556"
CERT_DIR = Path.home() / ".gans" / "certs"


def run_curve_rep_server():
    ctx = zmq.Context()
    auth = ThreadAuthenticator(ctx)
    auth.start()
    auth.configure_curve(domain="*", location=str(CERT_DIR / "clients"))

    server_key_file = list((CERT_DIR / "server").glob("*.key_secret"))[0]
    server_public, server_secret = zmq.auth.load_certificate(server_key_file)

    sock = ctx.socket(zmq.REP)
    sock.curve_publickey = server_public
    sock.curve_secretkey = server_secret
    sock.curve_server = True
    sock.bind(ADDR)

    msg = sock.recv_string()
    print(f"[SERVER] received: {msg!r}")
    sock.send_string(json.dumps({"type": "snapshot", "value": 99}))
    sock.close()
    auth.stop()
    ctx.term()


def main():
    app = QApplication(sys.argv)

    t = threading.Thread(target=run_curve_rep_server, daemon=True)
    t.start()

    client_public, client_secret = zmq.auth.load_certificate(
        str(CERT_DIR / "clients" / "gui.key_secret")
    )
    server_public, _ = zmq.auth.load_certificate(
        str(CERT_DIR / "server" / "server.key")
    )
    curve_keys = (client_public, client_secret, server_public)

    req = QtRequester(ADDR, curve_keys=curve_keys)

    def on_response(resp):
        print(f"[CLIENT] response: {resp}")
        assert resp.get("value") == 99
        print("[PASS] CURVE request -> response works correctly")
        app.quit()

    def on_error(e):
        print(f"[FAIL] error: {e}")
        app.quit()

    req.response.connect(on_response)
    req.error.connect(on_error)

    QTimer.singleShot(200, lambda: req.request("snapshot"))
    QTimer.singleShot(5000, lambda: (print("[FAIL] timeout"), app.quit()))

    sys.exit(app.exec())


if __name__ == "__main__":
    main()