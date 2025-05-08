import time, logging, zmq, argparse
from typing import List, Dict
from _01_project._99_helper.helper import conv_sensor_type_enum_2_str, conv_sig_value, conv_sensor_sig_unit_enum_2_str
from logger import Logger
from _01_project._02_sensor import sensor_message_pb2 as sensor_msg
import asyncio, zmq, sys, zmq.asyncio
from datetime import datetime as dt


class SensorServer:
    def __init__(self, log_file_path: str = None):
        if sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        # Init Logger
        self.log = Logger()
        if log_file_path:
            self.log._initialize(log_file_path)

        # Init Connection
        self.ctx_sub = zmq.asyncio.Context()
        self.ctx_req = zmq.asyncio.Context()

        self.sub_socket = self.ctx_sub.socket(zmq.SUB)
        self.sub_socket.bind("tcp://*:5550")
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

        self.rep_socket = self.ctx_req.socket(zmq.REP)
        self.rep_socket.bind("tcp://*:5551")

        self.socket_data_transf = None

        # Init Messages
        self.sensor_comJoin_structure = sensor_msg.ComJoin()
        self.sensor_comJoinResp_structure = sensor_msg.ComJoinResp()
        self.sensor_data_structure = sensor_msg.SensorStatus()

        # Attributes:
        self.sensor_values: List[Dict] = []
        self.new_sensor_id = 1

        self.log.log(msg="INIT Sensor Server correctly ...", level=logging.INFO)


    async def _rep_responder(self):
        while True:
            # Wait for next request from client
            message = await self.rep_socket.recv()
            self.sensor_comJoin_structure.ParseFromString(message)

            self.log.log(msg=f"[CONNECT_REQ] Received Sensor request to connect. "
                            f"Type: {conv_sensor_type_enum_2_str(self.sensor_comJoin_structure.type)}"
                            f", Sample_Frequency: {self.sensor_comJoin_structure.sample_freq}", level=logging.INFO)
            new_sensor_dict = dict(id=self.new_sensor_id,
                                   sample_freq=self.sensor_comJoin_structure.sample_freq,
                                   type=self.sensor_comJoin_structure.type)
            self.sensor_values.append(new_sensor_dict)
            time.sleep(0.5)
            self.sensor_comJoinResp_structure.sensor_id = self.new_sensor_id

            #  Send reply back to client
            self.log.log(msg=f"[CONNECT_REQ] Sending response: Sensor registration ID: {self.sensor_comJoinResp_structure.sensor_id}",
                        level=logging.INFO)
            self.rep_socket.send(self.sensor_comJoinResp_structure.SerializeToString())
            self.new_sensor_id += 1

    async def _sub_listener(self):
        while True:
            message = await self.sub_socket.recv()
            self.sensor_data_structure.ParseFromString(message)
            data = self.sensor_data_structure
            self.log.log(msg=f"[DATA_TRANSFER] Received Sensor Data of ID {data.id}: "
                             f"TimeStamp: {dt.fromtimestamp(data.timestamp / 100)} ({data.timestamp}), "
                             f"Factor: {data.factor}, Offset: {data.offset}, "
                             f"signal_value: {data.sig_value} - "
                             f"{(conv_sig_value(factor=data.factor/100, offset=data.offset/100, value=data.sig_value)):.2f} "
                             f"{conv_sensor_sig_unit_enum_2_str(data.sig_unit)}", level=logging.INFO)

    async def run_server(self):
        self.log.log(msg="[SERVER] Sensor Server running ...", level=logging.INFO)
        await asyncio.gather(
            self._sub_listener(),
            self._rep_responder()
        )

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
    asyncio.run(sensor_server.run_server())