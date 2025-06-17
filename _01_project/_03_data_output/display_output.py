import logging, argparse
from _01_project._99_helper.helper import conv_sensor_type_enum_2_str
import asyncio, zmq, sys, zmq.asyncio

class Display:
    def __init__(self):
        if sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        # Init Logger
        # no Logger needed

        # Init Connection
        self.ctx_pull = zmq.asyncio.Context()

        self.pull_socket = self.ctx_pull.socket(zmq.PULL)
        self.pull_socket.bind("tcp://*:5553")

    async def _data_pull_responder(self):
        while True:
            # Wait for next request from client
            message = await self.pull_socket.recv()
            topic, raw_data = message.split(b" ", 1)  # topic: 1 -> Registration Sensor | 2 -> Data
            if topic == b'1':
                self.sens_reg_structure.ParseFromString(raw_data)
                data = self.sens_reg_structure
                new_sensor = SensorItem(ident=data.connect, sample_freq=data.sample_freq, type=conv_sensor_type_enum_2_str(data.type))
                self.sensor_database.append(new_sensor)
                self.log.log(msg=f"[NEW_SENSOR] Received Sensor request to connect. "
                                 f"Type: {conv_sensor_type_enum_2_str(data.type)}"
                                 f", Sample_Frequency: {data.sample_freq}", level=logging.INFO)

    async def run_server(self):
        await asyncio.gather(
            self._data_pull_responder()
        )

def parse_args():
    # Argumentparser initialisieren
    parser = argparse.ArgumentParser(description="Verarbeitet Log-Dateien aus einem angegebenen Verzeichnis.")
    parser.add_argument('--log-dir', type=str, required=True, help="The path contains the log directory.")

    # Argumente parsen
    args = parser.parse_args()
    return args.log_dir

if __name__ == "__main__":
        log_dir = parse_args()
        sensor_server = Display()
        asyncio.run(sensor_server.run_server())
