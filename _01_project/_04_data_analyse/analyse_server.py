import logging, argparse
from typing import List
from logger import Logger
from _01_project._99_helper.helper import (conv_sig_value, conv_sensor_sig_unit_enum_2_str, conv_sensor_type_enum_2_str,
                                           conv_sensor_type_str_2_enum)
from _01_project._00_data_structure.data_structure import SensorItem, SensorStatus
from _01_project._00_data_structure import message_pb2 as nc_msg
import asyncio, zmq, sys, zmq.asyncio

class AnalyseServer:
    def __init__(self, log_file_path: str = None):
        if sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        # Init Logger
        self.log = Logger(external_log_file=log_file_path, sub_proc_name="ANALYSE_SERVER")

        # Init Connection
        self.ctx_pull = zmq.asyncio.Context()
        self.ctx_push = zmq.asyncio.Context()

        self.pull_socket = self.ctx_pull.socket(zmq.PULL)
        self.pull_socket.bind("tcp://*:5553")

        self.disp_push_socket = self.ctx_push.socket(zmq.PUSH)
        self.disp_push_socket.connect("tcp://localhost:5554")


        # Init Messages
        self.data_transfer_structure = nc_msg.sens_status()
        self.sens_reg_structure = nc_msg.sens_com_join()
        self.disp_trans_done = nc_msg.disp_trans_done()
        self.disp_disp_sensor_status = nc_msg.disp_sensor_status()

        # Attributes:
        self.sensor_database: List[SensorItem] = []

        self.log.log(msg="INIT Analyse Server correctly ...", level=logging.INFO)

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
            elif topic == b'2':
                self.data_transfer_structure.ParseFromString(raw_data)
                data = self.data_transfer_structure
                tmp_status = SensorStatus(timestamp=data.timestamp, id=data.id, factor=data.factor, offset=data.offset,
                                                 sig_value=data.sig_value, sig_unit=data.sig_unit)

                self.log.log(msg=f"[DATA_TRANS] Received Sensor Data -- "
                                 f"Time: {tmp_status.timestamp} - Sensor ID: Sensor {tmp_status.id} - "
                                 f"Value: {conv_sig_value(value=tmp_status.sig_value, factor= tmp_status.factor, offset=tmp_status.offset) }"
                                 f" {conv_sensor_sig_unit_enum_2_str(tmp_status.sig_unit)}", level=logging.INFO)

                self._append_status_to_sensor(status=tmp_status, active=1 if data.active == 1 else 0)

    async def _display_push_data(self):
        while True:
            await asyncio.sleep(4)
            if len(self.sensor_database) >= 1:
                for sensor in self.sensor_database:
                    data = sensor.data[-1]
                    self.disp_disp_sensor_status.sensor_id = sensor.id
                    self.disp_disp_sensor_status.sample_freq = sensor.sample_freq
                    self.disp_disp_sensor_status.type = conv_sensor_type_str_2_enum(sensor.type)
                    self.disp_disp_sensor_status.active = sensor.active
                    self.disp_disp_sensor_status.timestamp = data.timestamp
                    self.disp_disp_sensor_status.sig_value = data.sig_value
                    self.disp_disp_sensor_status.factor = data.factor
                    self.disp_disp_sensor_status.offset = data.offset
                    self.disp_disp_sensor_status.sig_unit = data.sig_unit #Todo Revert Fucntion
                    self.disp_disp_sensor_status.lower_threshold = 0#sensor.lower_threshold
                    self.disp_disp_sensor_status.upper_threshold = 0#sensor.upper_threshold
                    self.disp_disp_sensor_status.threshold_status = 0#data.threshold_status #TODO IF Verzweigung

                    await self.disp_push_socket.send("2".encode() + b" " + self.disp_disp_sensor_status.SerializeToString())
                self.disp_trans_done.done = 1
                await self.disp_push_socket.send("1".encode() + b" " + self.disp_trans_done.SerializeToString())
                self.log.log(msg=f"[DATA_TRANSFER] Pass Data to Analyse Server", level=logging.INFO)

    def _append_status_to_sensor(self, status: SensorStatus, active):
        for item in self.sensor_database:
            if item.id == status.id:
                item.append_sensor_value(status)
                item.set_active(active)
                return
        self.log.log(msg=f"[UNREGISTERED SENSOR] No SensorItem found with ID {status.id}. Status not appended.", level=logging.ERROR)

    async def run_server(self):
        self.log.log(msg="[SERVER] Analyse Server running ...", level=logging.INFO)
        await asyncio.gather(
            self._data_pull_responder(),
            self._display_push_data()
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
    sensor_server = AnalyseServer(log_file_path=log_dir)
    asyncio.run(sensor_server.run_server())