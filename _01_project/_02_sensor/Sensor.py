import random
from enum import Enum
from abc import ABC
import time, logging
from logger import Logger
import sensor_message_pb2 as sensor_msg

class SensorType(Enum):
    """Enumeration for different types of sensors."""
    PRESSURE = 1
    TEMPERATURE = 2
    ROTATION = 3

class Sensor(ABC):
    """A class representing a generic sensor."""
    def __init__(self, sensor_type: SensorType, offset:float, factor:float, unit:str, min_value_area: int,
                 max_value_area: int, send_freq_ms:int, log_file_path:str=None ):
        """
        Initialize a sensor.
        """
        self.id: int
        self.type: SensorType = sensor_type
        self.offset: float = offset
        self.factor: float = factor
        self.unit = unit
        self.value: int
        self._min_value: int = min_value_area
        self._max_value: int = max_value_area
        self._previous_values:list = []
        self._send_frequency = send_freq_ms
        self.connected = False

        # Init Logger
        self.log = Logger()
        if log_file_path:
            self.log._initialize(log_file_path)
        self.log.log(msg=f"Init new Sensor of type {sensor_type}", level=logging.INFO)

        self._connect()
        while(1):
            self._generate_value()
            self._send_data()
            time.sleep(self._send_frequency/1000)

    def _connect(self):
        """Simulate connecting the sensor."""
        self.connected = True
        self.id =1


    def _generate_value(self):
        self._previous_values.append(random.uniform(self._min_value, self._max_value))

        if len(self._previous_values) > 6:
            self._previous_values.pop(0)

        # Mittelwert berechnen
        raw_value = sum(self._previous_values) / len(self._previous_values)

        self.value = (self.factor * raw_value) + self.offset
        self.log.log(msg=f"Sensor no. {self.id} new measured data. value = {self.value}", level=logging.INFO)

    def _send_data(self):
        self.log.log(msg=f"Sending data from sensor {self.id}: {self.value:.2f} {self.unit}", level=logging.INFO)

class TempSensor(Sensor):
    def __init__(self):
        super().__init__(sensor_type=SensorType.TEMPERATURE,
                         offset=5.0,
                         factor=1.0,
                         unit=sensor_msg.sensor_signal_unit.UNIT_TEMP_CELSIUS,
                         min_value_area=0,
                         max_value_area=50,
                         send_freq_ms=1000)

class PresSensor(Sensor):
    def __init__(self):
        super().__init__(sensor_type=SensorType.TEMPERATURE,
                       offset=0.0,
                       factor=1.0,
                       unit=sensor_msg.sensor_signal_unit.UNIT_PRES_BAR,
                       min_value_area=1,
                       max_value_area=10,
                       send_freq_ms=20000)

class RotSensor(Sensor):
    def __init__(self):
        super().__init__(sensor_type=SensorType.TEMPERATURE,
                         offset=0.0,
                         factor=1.0,
                         unit=sensor_msg.sensor_signal_unit.UNIT_ROTA_RPM,
                         min_value_area=0,
                         max_value_area=1500,
                         send_freq_ms=500)

# Example usage
if __name__ == "__main__":
    temp_sensor = TempSensor()
    print(1)
