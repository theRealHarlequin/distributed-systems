# client_resp.py
import time
import zmq
import logging, threading, os, sys
from logger import Logger

# Initialize logger
log_file_path = sys.argv[1] if len(sys.argv) > 1 else None
log = Logger()
if log_file_path:
    log._initialize(log_file_path)

log.log("Subprocess started.")

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
