from dataclasses import dataclass
from typing import List, Optional
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

    @property
    def encoded_value(self) -> float:
        """Gets the signal unit."""
        return (self.factor * self._sig_value + self.offset) / 1000

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
        data (List[SensorStatus]): The actual data collected.
        active (bool): Whether the sensor is currently active.
        lower_threshold (int): Lower threshold for triggering events.
        upper_threshold (int): Upper threshold for triggering events.
    """

    def __init__(self, ident: int, sample_freq: float, type: str, lower_thre:int=None, upper_the:int=None):
        self._id: int = ident
        self._sample_freq: float = sample_freq
        self._type: str = type
        self._data: List[SensorStatus] = []
        self._active: bool = True
        self._lower_threshold: int = lower_thre
        self._upper_threshold: int = upper_the

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

    @property
    def active(self) -> bool:
        """Info about registraion of Sensor."""
        return self._active
    @property
    def lower_threshold(self) -> Optional[int]:
        return self._lower_threshold

    @lower_threshold.setter
    def lower_threshold(self, value: int):
        self._lower_threshold = value

    @property
    def upper_threshold(self) -> Optional[int]:
        return self._upper_threshold

    @upper_threshold.setter
    def upper_threshold(self, value: int):
        self._upper_threshold = value

    def set_active(self, active):
        self._active = active

    def append_sensor_value(self, value: SensorStatus):
        self.data.append(value)

@dataclass
class StatusDisplayItem:
    """
    Data container for displaying the real-time status of a sensor signal.

    Attributes:
        sensor_id (int): Unique identifier of the sensor.
        sample_freq (int): Sampling frequency of the sensor data in sec.
        type (str): Type or category of the sensor (e.g., "temperature").
        active (bool): Indicates whether the sensor is currently active.
        timestamp (int): Unix timestamp in milliseconds when the reading was taken.
        sig_value (int): Current signal value from the sensor.
        factor (int): Scaling factor to apply to the raw signal value.
        offset (int): Offset to add to the scaled signal value.
        sig_unit (str): Unit of the signal value (e.g., "°C").
        lower_threshold (int): Lower limit for threshold checking.
        upper_threshold (int): Upper limit for threshold checking.
        threshold_status (str): Status describing if the current signal is within thresholds
    """

    def __init__(self, sensor_id: int, sample_freq: int, type: str, active: bool,
                 timestamp: int, sig_value: int, factor: int, offset: int,
                 sig_unit: str, lower_threshold: str, upper_threshold: str, threshold_status: str):
        self._sensor_id: int = sensor_id
        self._sample_freq: int = sample_freq
        self._type: str = type
        self._active: bool = active
        self._timestamp: int = timestamp
        self._sig_value: int = sig_value
        self._factor: int = factor
        self._offset: int = offset
        self._sig_unit: str = sig_unit
        self._lower_threshold: str = lower_threshold
        self._upper_threshold: str = upper_threshold
        self._threshold_status: str = threshold_status

    @property
    def sensor_id(self) -> int:
        """Unique identifier for the sensor."""
        return self._sensor_id

    @property
    def sample_freq(self) -> int:
        """Sampling frequency in Hz."""
        return self._sample_freq

    @property
    def type(self) -> str:
        """Sensor type/category."""
        return self._type

    @property
    def active(self) -> bool:
        """Indicates whether the sensor is currently active."""
        return self._active

    @property
    def timestamp(self) -> int:
        """Timestamp of the reading in milliseconds since epoch."""
        return self._timestamp

    @property
    def sig_value(self) -> int:
        """Raw signal value."""
        return self._sig_value

    @property
    def factor(self) -> int:
        """Scaling factor for the signal."""
        return self._factor

    @property
    def offset(self) -> int:
        """Offset for the signal value."""
        return self._offset

    @property
    def sig_unit(self) -> str:
        """Unit of measurement for the signal (e.g., °C)."""
        return self._sig_unit

    @property
    def lower_threshold(self) -> str:
        """Lower threshold limit for signal value."""
        return self._lower_threshold

    @property
    def upper_threshold(self) -> str:
        """Upper threshold limit for signal value."""
        return self._upper_threshold

    @property
    def threshold_status(self) -> str:
        """Status indicating threshold compliance."""
        return self._threshold_status
