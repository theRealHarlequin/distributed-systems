import zmq
import random
import time
import sys
import temp_message_pb2 as temp_message

if len(sys.argv) != 3:
	print("Wrong number of command line arguments")
	exit()

context = zmq.Context()

# Socket to send messages on
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")

# Socket with direct access to the sink: used to synchronize start of batch
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

msg = temp_message.Temp()
msg.temp_unit = temp_message.Temp_Unit.TEMP_UNIT_CELSIUS

# print("[Sender] Press Enter when the workers are ready: ")
# _ = input()


# The first message is the number of tasks and signals start of batch
ntasks = sys.argv[1]
tasksize = sys.argv[2]
print(f"[Sender] Sending {ntasks} tasks of size {tasksize} to workers...")
sink.send(str.encode(ntasks))

# Initialize random number generator
random.seed()

# Send tasks
for task_nbr in range(int(ntasks)):
    msg.temp_value[:] = random.sample(range(int(tasksize)), int(tasksize))
    sender.send(msg.SerializeToString())
    print(f"[Sender] Sent task #{task_nbr} ...")


# Give 0MQ time to deliver
time.sleep(1)
