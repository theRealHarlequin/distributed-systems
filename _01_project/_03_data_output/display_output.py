import logging, argparse
from datetime import datetime
from _01_project._03_data_output.console_table import ConsoleTable
from typing import List
from _01_project._00_data_structure.data_structure import StatusDisplayItem
from _01_project._99_helper.helper import conv_sensor_type_enum_2_str, conv_threshold_status_enum_2_str, conv_sig_value, conv_sensor_sig_unit_enum_2_str
from _01_project._00_data_structure import message_pb2 as nc_msg
import asyncio, zmq, sys, zmq.asyncio

class Display:
    def __init__(self):
        if sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        # Init Logger
        # no Logger needed

        # Init Connection
        self.ctx_pull = zmq.asyncio.Context()

        self.pull_socket = self.ctx_pull.socket(zmq.PULL)
        self.pull_socket.bind("tcp://*:5554")

        # Variables
        title = """                                                               _ _             _             
                                                              (_) |           (_)            
         ___  ___ _ __  ___  ___  _ __   _ __ ___   ___  _ __  _| |_ ___  _ __ _ _ __   __ _ 
        / __|/ _ \ '_ \/ __|/ _ \| '__| | '_ ` _ \ / _ \| '_ \| | __/ _ \| '__| | '_ \ / _` |
        \__ \  __/ | | \__ \ (_) | |    | | | | | | (_) | | | | | || (_) | |  | | | | | (_| |
        |___/\___|_| |_|___/\___/|_|    |_| |_| |_|\___/|_| |_|_|\__\___/|_|  |_|_| |_|\__, |
                                                                                        __/ |
                                                                                       |___/ 
        """
        headers = ['Sensor ID', 'Sensor Type', 'Frequency', 'Timestamp', ' Value', ' Unit', 'lower threshold',
                   'upper threshold', 'status threshold']
        self._output_table: ConsoleTable = ConsoleTable(title=title, headers=headers)
        self._display_list:List[StatusDisplayItem] = []

        self.input_disp_trans_done = nc_msg.disp_trans_done()
        self.input_disp_sensor_status = nc_msg.disp_sensor_status()

    async def _data_pull_responder(self):
        while True:
            # Wait for next request from client
            message = await self.pull_socket.recv()
            topic, raw_data = message.split(b" ", 1)  # topic: 1 -> number of sensors | 2 -> Data
            if topic == b'1':
                self.input_disp_trans_done.ParseFromString(raw_data)
                if self.input_disp_trans_done.done == 1:
                    str_lst = []
                    for itm in self._display_list:
                        str_lst.append([str(itm.sensor_id), str(itm.type), str(itm.sample_freq),
                                        datetime.fromtimestamp(itm.timestamp/100).strftime("%Y-%m-%d %H:%M:%S"),
                                        conv_sig_value(value=itm.sig_value, factor=itm.factor/1000, offset=itm.offset/1000),
                                        conv_sensor_sig_unit_enum_2_str(itm.sig_unit), itm.lower_threshold,
                                        itm.upper_threshold, conv_threshold_status_enum_2_str(itm.threshold_status)])
                    self._output_table.add_rows(str_lst)
                    self._output_table.display()
                    self._display_list.clear()
            elif topic == b'2':
                self.input_disp_sensor_status.ParseFromString(raw_data)
                data = self.input_disp_sensor_status
                self._display_list.append(StatusDisplayItem(sensor_id=data.sensor_id, sample_freq=data.sample_freq,
                                                            type=conv_sensor_type_enum_2_str(data.type),
                                                            active=data.active, timestamp=data.timestamp, sig_value=data.sig_value,
                                                            factor=data.factor, offset=data.offset, sig_unit=data.sig_unit,
                                                            lower_threshold=str(data.lower_threshold) if data.lower_threshold > 0 else "",
                                                            upper_threshold=str(data.upper_threshold) if data.upper_threshold > 0 else "",
                                                            threshold_status=conv_threshold_status_enum_2_str(data.threshold_status)))


    async def run_server(self):
        await asyncio.gather(
            self._data_pull_responder()
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
        display = Display()
        asyncio.run(display.run_server())
