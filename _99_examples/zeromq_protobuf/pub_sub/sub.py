import zmq
import temp_message_pb2 as temp_message
import sys

if len(sys.argv) != 3:
	print("Wrong number of command line arguments")
	exit()

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.SUB)
socket.bind("tcp://*:5560")
#socket.setsockopt(zmq.SUBSCRIBE, str.encode(sys.argv[2]))
socket.setsockopt_string(zmq.SUBSCRIBE, sys.argv[2])

msg = temp_message.Temp()

while True:
    print("[Subscriber #", sys.argv[1],"] Waiting for publisher #", sys.argv[2])
    [address, contents] = socket.recv_multipart()
    msg.ParseFromString(contents)
    print("[Subscriber #", sys.argv[1],"] Received", msg.temp_value, " from ", address.decode())
 
socket.close()
context.term()

