import time
import json
import zmq

ADDR = "tcp://127.0.0.1:8000"

ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)
sock.bind(ADDR)

print("Publisher running on", ADDR)

i = 0

while True:

    payload = {
        "type": "data",
        "value": i,
    }

    sock.send_json(payload)

    print("sent:", payload)

    i += 1
    time.sleep(1)