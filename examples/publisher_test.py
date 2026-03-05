import zmq
import time

ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)

sock.bind("tcp://*:6000")

print("Publisher running")

time.sleep(2)

while True:
    msg = {"hello": "world"}
    print("sending", msg)
    sock.send_json(msg)
    time.sleep(1)