# server_req.py
import zmq
from logger import Logger
import logging, threading, os, sys

# Initialize logger
log_file_path = sys.argv[1] if len(sys.argv) > 1 else None
log = Logger()
if log_file_path:
    log._initialize(log_file_path)

log.log("Subprocess started.")

threading.current_thread().name = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for request in range(10):
    log.log(f"Sending request {request} ...", level=logging.INFO)
    socket.send_string("Hello")

    message = socket.recv()
    log.log(f"Received reply {request}: {message}", level=logging.INFO)
