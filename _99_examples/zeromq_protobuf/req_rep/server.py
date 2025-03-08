import time
import zmq
import temp_message_pb2 as temp_message

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

msg_req = temp_message.Temp_Request()
msg_rep = temp_message.Temp_Response()

print("[Server] Listening...")

while True:
	#  Wait for next request from client
	message = socket.recv()
	msg_req.ParseFromString(message)
	print("[Server] Received request: ", msg_req.temp_unit, " ", msg_req.nvalues)

	#  Do some 'work'
	time.sleep(1)

	msg_rep.temp_unit = temp_message.Temp_Unit.TEMP_UNIT_CELSIUS
	msg_rep.nvalues = 3
	for i in range(msg_rep.nvalues):
		msg_rep.temp_value.append(37 + i)

	#  Send reply back to client
	print("[Server] Sending response: ", msg_rep.temp_unit, " ", msg_rep.nvalues, " ", msg_rep.temp_value)
	socket.send(msg_rep.SerializeToString())
