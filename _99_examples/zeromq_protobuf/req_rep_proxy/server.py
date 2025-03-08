import time
import zmq
import sys
import temp_message_pb2 as temp_message

if len(sys.argv) != 2:
	print("Wrong number of command line arguments")
	exit()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5560")

msg_req = temp_message.Temp_Request()
msg_rep = temp_message.Temp_Response()

print("[Server #", sys.argv[1],"] Listening...")

while True:
	#  Wait for next request from client
	message = socket.recv()
	msg_req.ParseFromString(message)
	print("[Server #", sys.argv[1],"] Received request: ", msg_req.temp_unit, " ", msg_req.nvalues)

	#  Do some 'work'
	time.sleep(1)

	msg_rep.temp_unit = temp_message.Temp_Unit.TEMP_UNIT_CELSIUS
	msg_rep.nvalues = 3 + int(sys.argv[1])
	del msg_rep.temp_value[:]
	for i in range(msg_rep.nvalues):
		msg_rep.temp_value.append(37 + i)

	#  Send reply back to client
	print("[Server #", sys.argv[1],"] Sending response: ", msg_rep.temp_unit, " ", msg_rep.nvalues, " ", msg_rep.temp_value)
	socket.send(msg_rep.SerializeToString())
