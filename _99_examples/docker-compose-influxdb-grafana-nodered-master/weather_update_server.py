import zmq
from random import randrange
import time


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

while True:
    zipcode = randrange(1, 10)
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)

    socket.send_string(f"{zipcode}", flags=zmq.SNDMORE)
    socket.send_string(f"{temperature}")
    if zipcode == 5:
        print(temperature)
    time.sleep(0.1)

socket.close()
context.term()
