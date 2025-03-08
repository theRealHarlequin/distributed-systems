import zmq
import temp_message_pb2 as temp_message

context = zmq.Context()

#  Socket to talk to server
print("[Client] Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

msg_req = temp_message.Temp_Request()
msg_rep = temp_message.Temp_Response()


msg_req.temp_unit = temp_message.Temp_Unit.TEMP_UNIT_CELSIUS
msg_req.nvalues = 5
print("[Client] Sending request: ", msg_req.temp_unit, " ", msg_req.nvalues)
socket.send(msg_req.SerializeToString())

#  Get the reply.
message = socket.recv()
msg_rep.ParseFromString(message)
print("[Client] Received response: ", msg_rep.temp_unit, " ", msg_rep.nvalues, " ", msg_rep.temp_value)
	
	
