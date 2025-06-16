import logging, zmq, zmq.asyncio, asyncio, os, subprocess, time
from _99_helper.helper import get_all_sensor_var, conv_sensor_type_enum_2_str
from _02_data_source import sensor_message_pb2 as sensor_msg
from _01_project._01_com_manager import system_message_pb2 as system_msg
from logger import Logger

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
log = Logger()
central_log_path = log.get_log_file_path()

processes = []

log.log(msg="init_env", level=logging.INFO)
run_in_new_console = True

class sim_control:
    def __init__(self):
        # Get the directory of the current script
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.processes = []

        #Init Logger
        self.log = Logger()
        self.log_path = log.get_log_file_path()

        self.log.log(msg="init_env", level=logging.INFO)
        self.run_in_new_console = True

        self.ctx_req = zmq.Context()
        self.ctrl_req_socket = self.ctx_req.socket(zmq.REQ)
        self.ctrl_req_socket.connect("tcp://localhost:5552")

        self.ctrl_req_structure = system_msg.RSDBI()
        self.ctrl_resp_structure = system_msg.RSDBI_resp()

        self.menu_options = [("Add new sensor to the control system.", self._add_sensor_to_system),
                             ("Unsubscribe sensor from the control system.", self._unsubscribe_sensor),
                             ("Subscribe sensor from the control system.", self._subscribe_sensor),
                             ("Change the threshold value.", self._change_threshold_value),
                             ("Exit / Close Simulation.", self._exit_program)]

    def start_new_subprocess(self, script:str):
        script_path = os.path.join(current_dir, script)  # Ensure correct path
        log.log(msg=f"[SUBPROCESS] Starting: {script} at {script_path}", level=logging.INFO)
        if run_in_new_console:
            p = subprocess.Popen(["python", script_path, "--log-dir", self.log_path],
                                 start_new_session=True, creationflags=subprocess.CREATE_NEW_CONSOLE )
        else:
            p = subprocess.Popen(["python", script_path, self.log_path])

        processes.append(p)

    def _get_validated_input(self, prompt: str, min_value: int = None, max_value: int = None) -> int:
        while True:
            user_input = input(prompt)

            if user_input.strip().isdigit():
                value = int(user_input)
                if (min_value is not None and value < min_value):
                    print(f"Input must be >= {min_value}.")
                elif (max_value is not None and value > max_value):
                    print(f"Input must be <= {max_value}.")
                else:
                    return value
            else:
                print("Input must be an integer.")


    def _clear_console(self):
        """Clear the console output."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _add_sensor_to_system(self):
        print("Running - Add Sensor to System...")

        sensor_type_dict = get_all_sensor_var()
        sensor_list_str=""
        for key in get_all_sensor_var():
            sensor_list_str += f" {key} -> {sensor_type_dict[key]} |"
        print(f"Select Sensor Type: {sensor_list_str}")

        inp_sensor_type = self._get_validated_input(prompt=f"Sensor Type to create (0-2): ",
                                                min_value=0,
                                                max_value=2)
        print(f"Selected SensorType: {conv_sensor_type_enum_2_str(inp_sensor_type)} - Creating sensor...")
        #inp_default_setup = self._get_validated_input(prompt=f"SensorSetup as default values (1) or own values (0): ",
        #                                          min_value=0,
        #                                          max_value=1)
        #if inp_default_setup == 1:
        #    # Create a sensor on default values
        #
        #inp_send_freq = self._get_validated_input(prompt=f"What is the sensor frequency on the network (100...10'000ms): ",
        #                                      min_value=100,
        #                                      max_value=10000)
        #inp_offset = self._get_validated_input(prompt=f"How big is the Offset of the Sensor? Value = Factor * RawValue + Offset: ",
        #                                      min_value=0,
        #                                      max_value=1)
        #inp_factor = self._get_validated_input(prompt=f"How big is the Factor of the Sensor? Value = Factor * RawValue + Offset: ",
        #                                      min_value=0,
        #                                      max_value=1)
        #inp_min_value_area = self._get_validated_input(prompt=f"What is the smallest value of the sensor area? (between 0 and 1000): ",
        #                                      min_value=0,
        #                                      max_value=1000)
        #inp_max_value_area = self._get_validated_input(prompt=f"What is the highest value of the sensor area? (Greater than smallest) (between 0 and 1000):",
        #                                      min_value=0,
        #                                      max_value=1000)
        if inp_sensor_type == sensor_msg.sensor_type.TYPE_ROTATION:
            self.start_new_subprocess(script=r"_02_data_source/rotation_sensor.py")
        elif inp_sensor_type == sensor_msg.sensor_type.TYPE_TEMPERATURE:
            self.start_new_subprocess(script=r"_02_data_source/temperature_sensor.py")
        elif inp_sensor_type == sensor_msg.sensor_type.TYPE_PRESSURE:
            self.start_new_subprocess(script=r"_02_data_source/pressure_sensor.py")
        print("")
        input("Press Enter to return to the menu.")

    def _unsubscribe_sensor(self):
        print("Running - Unsubscribe Sensor...")
        id_2_unsub = self._get_validated_input(prompt=f"Sensor ID to unsubscribe : ", min_value=1, max_value=100)
        status = self._control_communication(req_id=system_msg.request_id.UNSUBSCRIBE_SENSOR_ID, value_0= id_2_unsub)
        if status:
            print(f"Unsubsciption of Sensor with ID: {id_2_unsub}.")
        else:
            print(f"Sensor with ID {id_2_unsub} is not part of the system anymore.")
        input("Press Enter to return to the menu.")

    def _subscribe_sensor(self):
        print("Running - subscribe Sensor...")
        id_2_sub = self._get_validated_input(prompt=f"Sensor ID to subscribe : ", min_value=1, max_value=100)
        status = self._control_communication(req_id=system_msg.request_id.SUBSCRIBE_SENSOR_ID, value_0=id_2_sub)
        if status:
            print(f"Subscibtion of Sensor with ID: {id_2_sub}.")
        else:
            print(f"Sensor with ID {id_2_sub} can not be subscibted.")
        input("Press Enter to return to the menu.")

    def _change_threshold_value(self):
        print("Running - Change Threshold Value...")
        input("Press Enter to return to the menu.")

    def _exit_program(self):
        print("Exiting program & killing all processes. Goodbye!")

        for p in processes:  # Kill all processes
            p.terminate()
        exit()

    def _control_communication(self, req_id: system_msg.request_id, value_0: int=0, value_1: int=0, value_2: int=0, value_3: int=0,
                                     value_4: int=0, value_5: int=0, value_6: int=0, value_7: int=0):
        self.ctrl_req_structure.id = req_id
        self.ctrl_req_structure.value_0 = 0
        self.ctrl_req_structure.value_1 = 0
        self.ctrl_req_structure.value_2 = 0
        self.ctrl_req_structure.value_3 = 0
        self.ctrl_req_structure.value_4 = 0
        self.ctrl_req_structure.value_5 = 0
        self.ctrl_req_structure.value_6 = 0
        self.ctrl_req_structure.value_7 = 0
        if req_id == system_msg.request_id.GET_SENSOR_MAX_ID:
            # Send Request
            self.ctrl_req_socket.send(self.ctrl_req_structure.SerializeToString())

            # Receive Response
            message = self.ctrl_req_socket.recv()
            self.ctrl_resp_structure.ParseFromString(message)

            if self.ctrl_resp_structure.id == req_id:
                return self.ctrl_resp_structure.value_0
            else:
                return None

        elif req_id == system_msg.request_id.UNSUBSCRIBE_SENSOR_ID:
            # Send Request
            self.ctrl_req_structure.value_0 = value_0
            self.ctrl_req_socket.send(self.ctrl_req_structure.SerializeToString())

            # Receive Response
            message = self.ctrl_req_socket.recv()
            self.ctrl_resp_structure.ParseFromString(message)

            if (self.ctrl_resp_structure.id == req_id and self.ctrl_resp_structure.value_0 == value_0 and self.ctrl_resp_structure.value_1 == 1):
                return 1
            else:
                return None

        elif req_id == system_msg.request_id.SUBSCRIBE_SENSOR_ID:
            # Send Request
            self.ctrl_req_structure.value_0 = value_0
            self.ctrl_req_socket.send(self.ctrl_req_structure.SerializeToString())

            # Receive Response
            message = self.ctrl_req_socket.recv()
            self.ctrl_resp_structure.ParseFromString(message)

            if (self.ctrl_resp_structure.id == req_id and self.ctrl_resp_structure.value_0 == value_0 and self.ctrl_resp_structure.value_1 == 1):
                return 1
            else:
                return None

        elif req_id == system_msg.request_id.GET_ALERT_THRESHOLD:
            pass
        elif req_id == system_msg.request_id.SET_ALERT_THRESHOLD:
            pass
        elif req_id == system_msg.request_id.DISPLAY_GRAPH:
            pass
        self.ctrl_req_socket.send(self.ctrl_resp_structure.SerializeToString())

    def main_menu(self):
        """Display the main menu and handle user input."""
        # start Server
        self.start_new_subprocess(script="_04_data_analyse/analyse_server.py")
        self.start_new_subprocess(script="_01_com_manager/sensor_server.py")

        # start loop
        while True:
            self._clear_console()
            print("=== Main Menu ===")
            for idx, (option_text, _) in enumerate(self.menu_options, start=1):
                print(f"{idx}. {option_text}")

            choice = input("Select an option: ")

            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.menu_options):
                    self._clear_console()
                    _, selected_function = self.menu_options[choice_num - 1]
                    selected_function()
                else:
                    print("Invalid selection. Please try again.")
                    input("Press Enter to continue.")
            else:
                print("Please enter a valid number.")
                input("Press Enter to continue.")


if __name__ == "__main__":
    simulation_control = sim_control()
    simulation_control.main_menu()
