import zmq


def main():
	""" main method """

	context = zmq.Context()

	# Socket facing subscribers
	frontend = context.socket(zmq.XPUB)
	frontend.bind("tcp://*:5559")

	# Socket facing publishers
	backend  = context.socket(zmq.XSUB)
	backend.bind("tcp://*:5560")

	print("[Proxy] Listening...")

	zmq.proxy(frontend, backend)

	# We never get here...
	frontend.close()
	backend.close()
	context.term()


if __name__ == "__main__":
    main()
