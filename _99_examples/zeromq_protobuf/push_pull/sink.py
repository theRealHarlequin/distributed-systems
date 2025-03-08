import sys
import time
import zmq
import temp_message_pb2 as temp_message

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

msg = temp_message.Temp()

# Wait for start of batch
ntasks = receiver.recv()
print(f"[Sink] Expecting {int(ntasks)} tasks")

# Start our clock now
tstart = time.time()

# Process 100 confirmations
for task_nbr in range(int(ntasks)):
	message = receiver.recv()
	msg.ParseFromString(message)
	print(f"[Sink] Received task #{task_nbr} consisting of {len(msg.temp_value)} values")
    

# Calculate and report duration of batch
tend = time.time()
print(f"[Sink] Total elapsed time: {(tend-tstart)*1000} msec")
