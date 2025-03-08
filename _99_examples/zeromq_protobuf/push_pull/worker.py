import sys
import time
import zmq
import temp_message_pb2 as temp_message

if len(sys.argv) != 2:
	print("Wrong number of command line arguments")
	exit()

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

print(f"[Worker #{sys.argv[1]}] running ...")


msg = temp_message.Temp()

# Process tasks forever
while True:
	message = receiver.recv()
	msg.ParseFromString(message)
	print("[Worker #", sys.argv[1], "] Received task consisting of", len(msg.temp_value), "values")

	#  Do some 'work'
	time.sleep(1)

	# Simple progress indicator for the viewer
	sys.stdout.write('.')
	sys.stdout.flush()

	# Do the work
	time.sleep(1)

	# Send results to sink
	sender.send(msg.SerializeToString())
