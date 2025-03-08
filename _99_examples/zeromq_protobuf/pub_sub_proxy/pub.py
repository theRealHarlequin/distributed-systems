import time
import zmq
import sys
import temp_message_pb2 as temp_message

if len(sys.argv) != 2:
	print("Wrong number of command line arguments")
	exit()

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://localhost:5560")

msg = temp_message.Temp()

msg.temp_value=100 * int(sys.argv[1])
msg.temp_unit = temp_message.Temp_Unit.TEMP_UNIT_CELSIUS

for i in range(5):
    print("[Publisher #", sys.argv[1],"] Sending ", msg.temp_value)
    socket.send_multipart([str.encode(sys.argv[1]), msg.SerializeToString()])
    msg.temp_value = msg.temp_value + 1
    time.sleep(1)

# We never get here but clean up anyhow
socket.close()
context.term()

