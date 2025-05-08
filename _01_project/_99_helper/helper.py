from _01_project._02_sensor import sensor_message_pb2 as sensor_msg
import enum


def conv_sensor_sig_unit_enum_2_str(enum_value :enum):
    unit = ""
    if enum_value == sensor_msg.sensor_signal_unit.UNIT_UNSPECIFIED:
        unit = ""
    elif enum_value == sensor_msg.sensor_signal_unit.UNIT_TEMP_KELVIN:
        unit = "°K"
    elif enum_value == sensor_msg.sensor_signal_unit.UNIT_TEMP_CELSIUS:
        unit = "°C"
    elif enum_value == sensor_msg.sensor_signal_unit.UNIT_PRES_BAR:
        unit = "bar"
    elif enum_value == sensor_msg.sensor_signal_unit.UNIT_PRES_PASCAL:
        unit = "pa"
    elif enum_value == sensor_msg.sensor_signal_unit.UNIT_ROTA_RPM:
        unit = "rpm"
    return unit


def conv_sensor_type_enum_2_str(enum_value: enum):
    sensor = ""
    if enum_value == sensor_msg.sensor_type.TYPE_TEMPERATURE:
        sensor = "Temperatur_Sensor"
    elif enum_value == sensor_msg.sensor_type.TYPE_PRESSURE:
        sensor = "Pressure_Sensor"
    elif enum_value == sensor_msg.sensor_type.TYPE_ROTATION:
        sensor = "Rotation_Sensor"
    return sensor

def get_all_sensor_var() -> dict:
    ret_dict = {}
    for sensor in sensor_msg.sensor_type:
        ret_dict[sensor] = conv_sensor_type_enum_2_str(sensor)
    return ret_dict


def conv_sig_value(value: float, factor: float, offset: float) -> float:
    return (value * int(factor * 1000) / 1000 + int(offset * 1000) / 1000)