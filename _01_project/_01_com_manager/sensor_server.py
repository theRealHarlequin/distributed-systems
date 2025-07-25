import time, logging, argparse, sys, os
import asyncio, zmq, sys, zmq.asyncio
from typing import List, Set

sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from logger import Logger
from _01_project._99_helper.helper import conv_sensor_type_enum_2_str, conv_ctrl_type_enum_2_str
from _01_project._00_data_structure import message_pb2 as nc_msg
from _01_project._00_data_structure.data_structure import SensorStatus



class SensorServer:
    def __init__(self, log_file_path: str = None):
        if sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        # Init Logger
        self.log = Logger(external_log_file=log_file_path, sub_proc_name="SENSOR_SERVER")

        # Init Connection
        self.ctx_sub = zmq.asyncio.Context()
        self.ctx_req = zmq.asyncio.Context()
        self.ctx_req_ctr = zmq.asyncio.Context()
        self.ctx_push = zmq.asyncio.Context()

        self.sens_sub_socket = self.ctx_sub.socket(zmq.SUB)
        self.sens_sub_socket.bind("tcp://*:5550")
        self._active_subscriptions: Set[str] = set()

        self.sens_rep_socket = self.ctx_req.socket(zmq.REP)
        self.sens_rep_socket.bind("tcp://*:5551")

        self.ctrl_rep_socket = self.ctx_req_ctr.socket(zmq.REP)
        self.ctrl_rep_socket.bind("tcp://*:5552")

        self.data_push_socket = self.ctx_push.socket(zmq.PUSH)
        self.data_push_socket.connect("tcp://localhost:5553")

        # Init Messages
        self.sensor_comJoin_structure = nc_msg.sens_com_join()
        self.sensor_comJoinResp_structure = nc_msg.sens_com_join_resp()
        self.sensor_data_structure = nc_msg.sens_status()
        self.ctrl_request_structure = nc_msg.ctrl_RSDBI()
        self.ctrl_response_structure = nc_msg.ctrl_RSDBI_resp()
        self.data_structure = nc_msg.sens_status()
        self.ctrl_trans_structure = nc_msg.ctrl_request_transfert()

        # Attributes:
        self.push_send_output: List[SensorStatus] = []
        self.new_sensor_id = 1

        self.log.log(msg="INIT Sensor Server correctly ...", level=logging.INFO)

    def _append_status_to_sensor(self, status: SensorStatus):
        for item in self.sensor_database:
            if item.id == status.id:
                item.append_sensor_value(status)
                return
        self.log.log(msg=f"[UNREGISTERED SENSOR] No SensorItem found with ID {status.id}. Status not appended.", level=logging.ERROR)

    def _append_status_buffer(self, status: SensorStatus):
        self.push_send_output.append(status)

    async def _sensor_rep_responder(self):
        while True:
            # Wait for next request from client
            message = await self.sens_rep_socket.recv()
            self.sensor_comJoin_structure.ParseFromString(message)

            self.log.log(msg=f"[CONNECT_REQ] Received Sensor request to connect. "
                             f"Type: {conv_sensor_type_enum_2_str(self.sensor_comJoin_structure.type)}"
                             f", Sample_Frequency: {self.sensor_comJoin_structure.sample_freq}", level=logging.INFO)
            sens_reg = self.sensor_comJoin_structure
            sens_reg.connect = self.new_sensor_id
            await self.data_push_socket.send("1".encode() + b" " + sens_reg.SerializeToString())

            # send response to Sensor
            self.sensor_comJoinResp_structure.sensor_id = self.new_sensor_id
            self.sens_sub_socket.setsockopt_string(zmq.SUBSCRIBE, str(self.new_sensor_id))
            self._active_subscriptions.add(str(self.new_sensor_id))

            #  Send reply back to client
            self.log.log(msg=f"[CONNECT_REQ] Sending response: Sensor registration ID: {self.sensor_comJoinResp_structure.sensor_id}",
                        level=logging.INFO)
            self.sens_rep_socket.send(self.sensor_comJoinResp_structure.SerializeToString())
            self.new_sensor_id += 1

    async def _control_rep_responder(self):
        while True:
            # Wait for next request from client
            message = await self.ctrl_rep_socket.recv()
            self.ctrl_request_structure.ParseFromString(message)

            self.log.log(msg=f"[CTRL_REQ] Received control request from MasterPannel. "
                             f"Type: {conv_ctrl_type_enum_2_str(self.ctrl_request_structure.id)}",
                         level=logging.INFO)

            if self.ctrl_request_structure.id == nc_msg.ctrl_request_id.GET_SENSOR_MAX_ID:
                self.ctrl_response_structure.id = self.ctrl_request_structure.id
                self.ctrl_response_structure.value_0 = max(self.sensor_database, key=lambda item: item.id).id
                self.log.log(msg=f"[CTRL_RESP] Sending response: number of sensors {self.ctrl_response_structure.value_0}",
                    level=logging.INFO)

                time.sleep(10)
                self.ctrl_rep_socket.send(self.ctrl_response_structure.SerializeToString())

            elif self.ctrl_request_structure.id == nc_msg.ctrl_request_id.UNSUBSCRIBE_SENSOR_ID:
                self.ctrl_response_structure.id = self.ctrl_request_structure.id
                self.ctrl_response_structure.value_0 = self.ctrl_request_structure.value_0
                self.ctrl_response_structure.value_1 = 1

                if str(self.ctrl_request_structure.value_0) in self._active_subscriptions:
                    self.sens_sub_socket.setsockopt_string(zmq.UNSUBSCRIBE, str(self.ctrl_request_structure.value_0))
                    self._active_subscriptions.discard(str(self.ctrl_request_structure.value_0))
                    self.log.log(
                        msg=f"[UNSUBSCRIBE_SENSOR] ID {self.ctrl_response_structure.value_0} has been unsubscribed",
                        level=logging.INFO)
                    self._append_status_buffer(SensorStatus(timestamp=0, id=self.ctrl_request_structure.value_0,
                                                            factor=0, offset=0, sig_value=0,
                                                            sig_unit=nc_msg.sens_signal_unit.UNIT_UNSPECIFIED))
                else:
                    self.log.log(
                        msg=f"[UNSUBSCRIBE_SENSOR] ID {self.ctrl_response_structure.value_0} no sensor with this id is registrated",
                        level=logging.ERROR)

                self.ctrl_rep_socket.send(self.ctrl_response_structure.SerializeToString())

            elif self.ctrl_request_structure.id == nc_msg.ctrl_request_id.SUBSCRIBE_SENSOR_ID:
                self.ctrl_response_structure.id = self.ctrl_request_structure.id
                self.ctrl_response_structure.value_0 = self.ctrl_request_structure.value_0
                self.ctrl_response_structure.value_1 = 1
                if str(self.ctrl_request_structure.value_0) not in self._active_subscriptions:
                    self.sens_sub_socket.setsockopt_string(zmq.SUBSCRIBE, str(self.ctrl_request_structure.value_0))
                    self._active_subscriptions.add(str(self.ctrl_request_structure.value_0))
                    self.log.log(msg=f"[SUBSCRIBE_SENSOR] ID {self.ctrl_response_structure.value_0} has been resubscribed.",
                        level=logging.INFO)
                else:
                    self.log.log(
                        msg=f"[SUBSCRIBE_SENSOR] ID {self.ctrl_response_structure.value_0} is already subscribed by the system.",
                        level=logging.ERROR)

                self.ctrl_rep_socket.send(self.ctrl_response_structure.SerializeToString())

            elif self.ctrl_request_structure.id == nc_msg.ctrl_request_id.SET_LOWER_THRESHOLD:
                self.ctrl_response_structure.id = self.ctrl_request_structure.id
                self.ctrl_response_structure.value_0 = self.ctrl_request_structure.value_0
                self.ctrl_response_structure.value_1 = self.ctrl_request_structure.value_1
                self.ctrl_response_structure.value_2 = 1
                self.ctrl_rep_socket.send(self.ctrl_response_structure.SerializeToString())

                self.ctrl_trans_structure.sensor_id = self.ctrl_request_structure.value_0
                self.ctrl_trans_structure.request_type = self.ctrl_request_structure.id
                self.ctrl_trans_structure.value = self.ctrl_request_structure.value_1

                await self.data_push_socket.send("3".encode() + b" " + self.ctrl_trans_structure.SerializeToString())
                self.log.log(msg=f"[CTRL_TRANSFER] Pass Control Request", level=logging.INFO)

            elif self.ctrl_request_structure.id == nc_msg.ctrl_request_id.SET_UPPER_THRESHOLD:
                self.ctrl_response_structure.id = self.ctrl_request_structure.id
                self.ctrl_response_structure.value_0 = self.ctrl_request_structure.value_0
                self.ctrl_response_structure.value_1 = self.ctrl_request_structure.value_1
                self.ctrl_response_structure.value_2 = 1
                self.ctrl_rep_socket.send(self.ctrl_response_structure.SerializeToString())

                self.ctrl_trans_structure.sensor_id = self.ctrl_request_structure.value_0
                self.ctrl_trans_structure.request_type = self.ctrl_request_structure.id
                self.ctrl_trans_structure.value = self.ctrl_request_structure.value_1

                await self.data_push_socket.send("3".encode() + b" " + self.ctrl_trans_structure.SerializeToString())
                self.log.log(msg=f"[CTRL_TRANSFER] Pass Control Request", level=logging.INFO)

            elif self.ctrl_request_structure.id == nc_msg.ctrl_request_id.DISPLAY_GRAPH:
                self.ctrl_response_structure.id = self.ctrl_request_structure.id
                self.ctrl_response_structure.value_0 = self.ctrl_request_structure.value_0
                self.ctrl_response_structure.value_1 = 1
                self.ctrl_rep_socket.send(self.ctrl_response_structure.SerializeToString())

                self.ctrl_trans_structure.sensor_id = self.ctrl_request_structure.value_0
                self.ctrl_trans_structure.request_type = self.ctrl_request_structure.id
                self.ctrl_trans_structure.value = 0

                await self.data_push_socket.send("3".encode() + b" " + self.ctrl_trans_structure.SerializeToString())
                self.log.log(msg=f"[CTRL_TRANSFER] Pass Control Request", level=logging.INFO)

    async def _sensor_sub_listener(self):
        while True:
            message = await self.sens_sub_socket.recv()
            topic, raw_data = message.split(b" ", 1)  # topic is the sensor ID

            self.sensor_data_structure.ParseFromString(raw_data)
            data = self.sensor_data_structure
            tmp_sensor_status = SensorStatus(timestamp=data.timestamp, id=data.id, factor=data.factor, offset=data.offset,
                               sig_value=data.sig_value, sig_unit=data.sig_unit)

            self._append_status_buffer(status=tmp_sensor_status)
            self.log.log(msg=f"[DATA_TRANSFER] Received Sensor Data of {tmp_sensor_status}", level=logging.INFO)

    async def _analyse_push(self):
        while True:
            await asyncio.sleep(2)
            tmp_lst: List[SensorStatus] = self.push_send_output[:]
            self.push_send_output.clear()
            for itm in tmp_lst:
                self.data_structure.id = itm.id
                self.data_structure.timestamp = itm.timestamp
                self.data_structure.sig_value = itm.sig_value
                self.data_structure.factor = itm.factor
                self.data_structure.offset = itm.offset
                self.data_structure.sig_unit = itm.sig_unit
                self.data_structure.active = 1 if str(itm.id) in self._active_subscriptions else 0

                await self.data_push_socket.send("2".encode() + b" " + self.data_structure.SerializeToString())
                self.log.log(msg=f"[DATA_TRANSFER] Pass Data to Analyse Server", level=logging.INFO)

    async def run_server(self):
        self.log.log(msg="[SERVER] Sensor Server running ...", level=logging.INFO)
        await asyncio.gather(
            self._analyse_push(),
            self._sensor_sub_listener(),
            self._sensor_rep_responder(),
            self._control_rep_responder()
        )

def parse_args():
    # Argumentparser initialisieren
    parser = argparse.ArgumentParser(description="Verarbeitet Log-Dateien aus einem angegebenen Verzeichnis.")

    # Argument für das Log-Verzeichnis hinzufügen
    parser.add_argument('--log-dir', type=str, required=True, help="The path contains the log directory.")

    # Argumente parsen
    args = parser.parse_args()
    return args.log_dir

if __name__ == "__main__":
    try:
        log_dir = parse_args()
        sensor_server = SensorServer(log_file_path=log_dir, )
        asyncio.run(sensor_server.run_server())
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
        raise

