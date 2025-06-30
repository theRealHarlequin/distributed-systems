from _01_project._00_data_structure import message_pb2 as nc_msg
import enum


def conv_sensor_sig_unit_enum_2_str(enum_value :enum):
    unit = ""
    if enum_value == nc_msg.sens_signal_unit.UNIT_UNSPECIFIED:
        unit = ""
    elif enum_value == nc_msg.sens_signal_unit.UNIT_TEMP_KELVIN:
        unit = "°K"
    elif enum_value == nc_msg.sens_signal_unit.UNIT_TEMP_CELSIUS:
        unit = "°C"
    elif enum_value == nc_msg.sens_signal_unit.UNIT_PRES_BAR:
        unit = "bar"
    elif enum_value == nc_msg.sens_signal_unit.UNIT_PRES_PASCAL:
        unit = "pa"
    elif enum_value == nc_msg.sens_signal_unit.UNIT_ROTA_RPM:
        unit = "rpm"
    elif enum_value == nc_msg.sens_signal_unit.TYPE_ANGLE:
        unit = "degree"
    return unit


def conv_sensor_type_enum_2_str(enum_value: enum):
    sensor = ""
    if enum_value == nc_msg.sens_type.TYPE_TEMPERATURE:
        sensor = "Temperatur_Sensor"
    elif enum_value == nc_msg.sens_type.TYPE_PRESSURE:
        sensor = "Pressure_Sensor"
    elif enum_value == nc_msg.sens_type.TYPE_ROTATION:
        sensor = "Rotation_Sensor"
    elif enum_value == nc_msg.sens_type.TYPE_ANGLE:
        sensor = "Angle_Sensor"
    return sensor


def conv_sensor_type_str_2_enum(sensor_str: str) -> nc_msg.sens_type:
    if sensor_str == "Temperatur_Sensor":
        return nc_msg.sens_type.TYPE_TEMPERATURE
    elif sensor_str == "Pressure_Sensor":
        return nc_msg.sens_type.TYPE_PRESSURE
    elif sensor_str == "Rotation_Sensor":
        return nc_msg.sens_type.TYPE_ROTATION
    elif sensor_str == "Angle_Sensor":
        return nc_msg.sens_type.TYPE_ANGLE
    else:
        raise ValueError(f"Unknown sensor type string: {sensor_str}")


def conv_threshold_status_enum_2_str(enum_value: enum):
    threshold = ""
    if enum_value == nc_msg.disp_threshold_status.NO_EVALUATION:
        threshold = "no check performed"
    elif enum_value == nc_msg.disp_threshold_status.VALUE_INSIDE_AREA:
        threshold = "value is inside area"
    elif enum_value == nc_msg.disp_threshold_status.VALUE_TO_HIGH:
        threshold = "value is to high"
    elif enum_value == nc_msg.disp_threshold_status.VALUE_TO_LOW:
        threshold = "value is to low"
    return threshold


def conv_ctrl_type_enum_2_str(enum_value: enum):
    system = ""
    if enum_value == nc_msg.ctrl_request_id.GET_SENSOR_MAX_ID:
        system = "number of sensors"
    elif enum_value == nc_msg.ctrl_request_id.UNSUBSCRIBE_SENSOR_ID:
        system = "unsubscripe sensor"
    elif enum_value == nc_msg.ctrl_request_id.SUBSCRIBE_SENSOR_ID:
        system = "subscripe new sensor"
    elif enum_value == nc_msg.ctrl_request_id.SET_LOWER_THRESHOLD:
        system = "set lower threshold of sensor"
    elif enum_value == nc_msg.ctrl_request_id.SET_UPPER_THRESHOLD:
        system = "set upper threshold of sensor"
    elif enum_value == nc_msg.ctrl_request_id.DISPLAY_GRAPH:
        system = "display graph in seperate window"
    return system


def get_all_sensor_var() -> dict:
    ret_dict = {}
    for sensor in nc_msg.sens_type.DESCRIPTOR.values:
        ret_dict[sensor.name] = sensor.index
    return ret_dict


def conv_sig_value(value: float, factor: float, offset: float) -> float:
    return (value * int(factor * 1000) / 1000 + int(offset * 1000) / 1000)