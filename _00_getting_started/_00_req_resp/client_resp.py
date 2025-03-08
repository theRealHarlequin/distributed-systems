# client_resp.py
import time
import zmq
import logging, threading, os
from logger import Logger

# Initialize logger
log = Logger()
threading.current_thread().name = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    log.log(f"Received request: {message}", level=logging.INFO)

    time.sleep(1)  # Simulate work

    socket.send_string("World")
    log.log("Sent response: World", level=logging.INFO)
