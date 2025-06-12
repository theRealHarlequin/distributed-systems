from dataclasses import dataclass
from typing import List

@dataclass
class SensorData:
    """
    Class representing sensor data with encapsulated attributes.

    Attributes:
        id (int): Unique identifier for the data sample.
        sample_freq (float): Sampling frequency in Hz.
        type (str): Type of the sensor or measurement.
        data (Any): The actual data collected, e.g., list of values.
    """

    def __init__(self, id: int, sample_freq: float, type: str):
        """
        Initializes a new instance of the SensorData class.

        Args:
            id (int): Unique identifier for the data sample.
            sample_freq (float): Sampling frequency in Hz.
            type (str): Type of the sensor or measurement.
            data (Any): The actual data collected.
        """
        self._id:int  = id
        self._sample_freq: float = sample_freq
        self._type: str = type
        self._data:List = []

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

