# server_req.py
import zmq
from logger import Logger
import logging, threading, os

# Initialize logger
log = Logger()
threading.current_thread().name = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for request in range(10):
    log.log(f"Sending request {request} ...", level=logging.INFO)
    socket.send_string("Hello")

    message = socket.recv()
    log.log(f"Received reply {request}: {message}", level=logging.INFO)
