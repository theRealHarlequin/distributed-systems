import random, zmq, logging, zmq.asyncio, asyncio, sys
from enum import Enum
from abc import ABC
from logger import Logger
from datetime import datetime as dt
import _01_project._00_data_structure.message_pb2 as nc_msg
from _01_project._99_helper.helper import conv_sensor_sig_unit_enum_2_str, conv_sensor_type_enum_2_str, conv_sig_value

class Sensor(ABC):
    """A class representing a generic sensor."""
    def __init__(self, sens_type: nc_msg.sens_type, offset:float, factor:float, unit:str, min_value_area: int,
                 max_value_area: int, send_freq_ms:int, log_file_path:str=None):

        ## Init Sensor
        self.id: int = 0
        self.type: nc_msg.sens_type = sens_type
        self.offset: float = offset
        self.factor: float = factor
        self.unit = unit
        self.value: int
        self.value_encod:float # calculated value: factor * value + offset
        self._min_value: int = min_value_area
        self._max_value: int = max_value_area
        self._previous_values:list = []
        self._sample_freq = send_freq_ms
        self.connected = False

        ## Init Connection
        self.ctx_req = zmq.asyncio.Context()
        self.ctx_pub = zmq.asyncio.Context()

        # REQ socket
        self.req_socket = self.ctx_req.socket(zmq.REQ)
        self.req_socket.connect("tcp://localhost:5551")

        # PUB socket
        self.pub_socket = self.ctx_pub.socket(zmq.PUB)
        self.pub_socket.connect("tcp://localhost:5550")

        # Init Messages
        self.sensor_comJoin_msg = nc_msg.sens_com_join()
        self.sensor_comJoinResp_msg = nc_msg.sens_com_join_resp()
        self.sensor_data_msg = nc_msg.sens_status()

        ## Init Logger
        self.log = Logger(external_log_file=log_file_path, sub_proc_name="SENSOR")
        self.log.log(msg=f"Init new Sensor of type [{conv_sensor_type_enum_2_str(sens_type)}]", level=logging.INFO)

    async def _connect(self):
        """Simulate connecting the sensor."""

        #  Socket to talk to server
        self.log.log(msg=f"[Client] Start Connection to Sensor Server ...", level=logging.INFO)

        self.sensor_comJoin_msg.connect = 1
        self.sensor_comJoin_msg.type = self.type
        self.sensor_comJoin_msg.sample_freq = self._sample_freq
        self.log.log(msg=f"[Client] Sending request: Communication Join", level=logging.INFO)
        self.req_socket.send(self.sensor_comJoin_msg.SerializeToString())

        #  Get the reply.
        message = await self.req_socket.recv()
        self.sensor_comJoinResp_msg.ParseFromString(message)
        self.log.log(msg=f"[Client] Received response: Sensor ID - {self.sensor_comJoinResp_msg.sensor_id}",
                     level=logging.INFO)
        self.connected = True
        self.id = self.sensor_comJoinResp_msg.sensor_id


    def _generate_value(self):
        self._previous_values.append(random.uniform(self._min_value, self._max_value))

        if len(self._previous_values) > 6:
            self._previous_values.pop(0)

        # Mittelwert berechnen
        self.value = int(sum(self._previous_values) / len(self._previous_values))

        self.value_encod = (self._conv_factor_two_dec() * self.value) + self._conv_offset_two_dec()

    def _conv_offset_two_dec(self) -> float:
        return int(self.value * 100) / 100

    def _conv_factor_two_dec(self) -> float:
        return int(self.value * 100) / 100

    async def _send_data(self):
        self.log.log(msg=f"Sending data from sensor {self.id}: raw value {self.value:.2f} - "
                         f"{conv_sig_value(factor=self.factor, offset=self.offset, value=self.value):.2f} "
                         f"{conv_sensor_sig_unit_enum_2_str(enum_value=self.unit)}", level=logging.INFO)

        # generate MSG
        self.sensor_data_msg.timestamp = int(dt.now().timestamp() * 100)
        self.sensor_data_msg.id = self.id
        self.sensor_data_msg.factor = int(self.factor * 1000)
        self.sensor_data_msg.offset = int(self.offset * 1000)
        self.sensor_data_msg.sig_unit = self.unit
        self.sensor_data_msg.sig_value = self.value

        self.pub_socket.send(str(self.sensor_data_msg.id).encode() + b" " + self.sensor_data_msg.SerializeToString())

    async def start(self):
        # Connect first
        await self._connect()

        # Give SUBs a moment to connect
        await asyncio.sleep(1)

        # Start cyclic publishing
        while True:
            self._generate_value()
            await self._send_data()
            await asyncio.sleep(self._sample_freq / 1000)

class TempSensor(Sensor):
    def __init__(self):
        super().__init__(sens_type=nc_msg.sens_type.TYPE_TEMPERATURE,
                         offset=5.0,
                         factor=1.0,
                         unit=nc_msg.sens_signal_unit.UNIT_TEMP_CELSIUS,
                         min_value_area=0,
                         max_value_area=50,
                         send_freq_ms=1000)

class PresSensor(Sensor):
    def __init__(self):
        super().__init__(sens_type=nc_msg.sens_type.TYPE_PRESSURE,
                         offset=0.0,
                         factor=1.0,
                         unit=nc_msg.sens_signal_unit.UNIT_PRES_BAR,
                         min_value_area=1,
                         max_value_area=10,
                         send_freq_ms=20000)

class RotSensor(Sensor):
    def __init__(self):
        super().__init__(sens_type=nc_msg.sens_type.TYPE_ROTATION,
                         offset=0.0,
                         factor=1.0,
                         unit=nc_msg.sens_signal_unit.UNIT_ROTA_RPM,
                         min_value_area=0,
                         max_value_area=1500,
                         send_freq_ms=500)

# Example usage
if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def main():
        temp_sensor = TempSensor()
        await temp_sensor.start()

    asyncio.run(main())
