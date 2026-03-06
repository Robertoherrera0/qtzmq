import time
import zmq

ADDR = "tcp://127.0.0.1:8000"

ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)
sock.bind(ADDR)

print("Publisher running on", ADDR)

i = 0

while True:

    metadata = {
        "type": "metadata",
        "data": {
            "scan_id": i,
            "sample": "Si wafer",
            "temperature": 300 + i
        }
    }

    status = {
        "type": "status",
        "state": "running",
        "step": i
    }

    sock.send_json(metadata)
    sock.send_json(status)

    print("sent:", metadata)
    print("sent:", status)

    i += 1
    time.sleep(1)