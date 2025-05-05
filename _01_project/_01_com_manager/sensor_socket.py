import time, logging, zmq, argparse

from logger import Logger
from _01_project._02_sensor import sensor_message_pb2 as sensor_msg

class SensorServer:
    def __init__(self, log_file_path: str = None):
        # Init Logger
        self.log = Logger()
        if log_file_path:
            self.log._initialize(log_file_path)

        # Init Connection
        context = zmq.Context()
        self.socket_com_join = context.socket(zmq.REP)
        self.socket_com_join.bind("tcp://*:5555")

        self.socket_data_transf = None

        # Init Messages
        self.sensor_comJoin = sensor_msg.ComJoin()
        self.sensor_comJoinResp = sensor_msg.ComJoinResp()
        self.sensor_data = sensor_msg.SensorStatus()

        # Attributes:
        self.seonsor_values:dict ={}
        self.new_sensor_id = 1

    def run_server(self,):
        # Init Logger
        self.log.log(msg=f"[Sensor_Server] Listening...", level=logging.INFO)

        while True:
            #  Wait for next request from client
            message = self.socket_com_join.recv()
            self.sensor_comJoin.ParseFromString(message)
            self.log.log(msg=f"[Sensor_Server] Received Sensor request to connect...", level=logging.INFO)

            time.sleep(1)
            self.sensor_comJoinResp.sensor_id = self.new_sensor_id
            self.new_sensor_id += 1

            #  Send reply back to client
            self.log.log(msg=f"[Sensor_Server] Sending response: Sensor registration ID: {self.sensor_comJoinResp.sensor_id}", level=logging.INFO)
            self.socket_com_join.send(self.sensor_comJoinResp.SerializeToString())


def parse_args():
    # Argumentparser initialisieren
    parser = argparse.ArgumentParser(description="Verarbeitet Log-Dateien aus einem angegebenen Verzeichnis.")

    # Argument für das Log-Verzeichnis hinzufügen
    parser.add_argument(
        '--log-dir',
        type=str,
        required=True,  # Muss angegeben werden
        help="Der Pfad zum Verzeichnis, das die Log-Dateien enthält."
    )

    # Argumente parsen
    args = parser.parse_args()
    return args.log_dir

if __name__ == "__main__":
    log_dir = parse_args()
    sensor_server = SensorServer(log_file_path=log_dir)
    sensor_server.run_server()