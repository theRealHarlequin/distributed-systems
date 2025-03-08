import zmq
import temp_message_pb2 as temp_message
import sys

if len(sys.argv) != 3:
	print("Wrong number of command line arguments")
	exit()

context = zmq.Context()

#  Socket to talk to server
print("[Client #", sys.argv[1],"] Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5559")

msg_req = temp_message.Temp_Request()
msg_rep = temp_message.Temp_Response()

for i in range(int(sys.argv[2])):
    msg_req.temp_unit = temp_message.Temp_Unit.TEMP_UNIT_CELSIUS
    msg_req.nvalues = 10 + int(sys.argv[1])
    print("[Client #", sys.argv[1],"] Sending request: ", msg_req.temp_unit, " ", msg_req.nvalues)
    socket.send(msg_req.SerializeToString())
    
    #  Get the reply.
    message = socket.recv()
    msg_rep.ParseFromString(message)
    print("[Client #", sys.argv[1],"] Received response: ", msg_rep.temp_unit, " ", msg_rep.nvalues, " ", msg_rep.temp_value)
	
	
