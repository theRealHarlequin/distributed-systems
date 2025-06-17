from dataclasses import dataclass
from typing import List
from datetime import datetime as dt
from _01_project._99_helper.helper import conv_sig_value

@dataclass
class SensorStatus:
    """
    Class representing the status of a sensor.

    Attributes:
        timestamp (int): Timestamp in microseconds.
        id (int): Unique identifier for the sensor.
        sig_value (int): The raw signal value.
        factor (int): Scaling factor.
        offset (int): Offset to be applied.
        sig_unit (str): Unit of the signal.
    """

    def __init__(self, timestamp: int, id: int, sig_value: int, factor: int, offset: int, sig_unit: str):
        self._timestamp = timestamp
        self._id = id
        self._sig_value = sig_value
        self._factor = factor
        self._offset = offset
        self._sig_unit = sig_unit

    @property
    def timestamp(self) -> int:
        """Gets the timestamp in microseconds."""
        return self._timestamp


    @property
    def id(self) -> int:
        """Gets the unique sensor ID."""
        return self._id


    @property
    def sig_value(self) -> int:
        """Gets the raw signal value."""
        return self._sig_value


    @property
    def factor(self) -> int:
        """Gets the scaling factor."""
        return self._factor

    @property
    def offset(self) -> int:
        """Gets the offset to be applied."""
        return self._offset


    @property
    def sig_unit(self) -> str:
        """Gets the signal unit."""
        return self._sig_unit

    def __str__(self):
        return (f"Sensor-ID {self.id}: TimeStamp: {dt.fromtimestamp(self.timestamp / 100)} ({self.timestamp}), "
               f"Factor: {self.factor}, Offset: {self.offset}, signal_value: {self.sig_value} - "
               f"{(conv_sig_value(factor=self.factor/100, offset=self.offset/100, value=self.sig_value)):.2f} ")


@dataclass
class SensorItem:
    """
    Class representing sensor data with encapsulated attributes.

    Attributes:
        id (int): Unique identifier for the data sample.
        sample_freq (float): Sampling frequency in Hz.
        type (str): Type of the sensor or measurement.
        data (List[SensorStatus]): The actual data collected, e.g., list of values.
    """

    def __init__(self, ident: int, sample_freq: float, type: str):
        """
        Initializes a new instance of the SensorData class.

        Args:
            ident (int): Unique identifier for the data sample.
            sample_freq (float): Sampling frequency in Hz.
            type (str): Type of the sensor or measurement.
            data (List[SensorStatus]): The actual data collected.
        """
        self._id: int = ident
        self._sample_freq: float = sample_freq
        self._type: str = type
        self._data: List = [SensorStatus]

    @property
    def id(self) -> int:
        """Gets the unique identifier of the data sample."""
        return self._id

    @property
    def sample_freq(self) -> float:
        """Gets the sampling frequency in Hz."""
        return self._sample_freq


    @property
    def type(self) -> str:
        """Gets the type of the sensor or measurement."""
        return self._type

    @property
    def data(self) -> List:
        """Gets the collected data."""
        return self._data

    def append_sensor_value(self, value: SensorStatus):
        self.data.append(value)