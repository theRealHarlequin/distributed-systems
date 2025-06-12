import logging
import subprocess
from _99_helper.helper import get_all_sensor_var, conv_sensor_type_enum_2_str
from _02_data_source import sensor_message_pb2 as sensor_msg
import os
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

        self.menu_options = [("Add new sensor to the control system.", self._add_sensor_to_system),
                             ("Remove sensor from the control system.", self._remove_sensor_of_system),
                             ("Change the threshold value.", self._change_threshold_value),
                             ("Exit / Close Simulation.", self._exit_program)]

    def start_new_subprocess(self, script:str):
        script_path = os.path.join(current_dir, script)  # Ensure correct path
        log.log(msg=f"start_process of {script} at {script_path}", level=logging.INFO)
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


    def clear_console(self):
        """Clear the console output."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _add_sensor_to_system(self):
        print("Running - Add Sensor to System...")

        sensor_type_dict = get_all_sensor_var()
        sensor_list_str=""
        for key in get_all_sensor_var():
            sensor_list_str += f"    {key} -> {sensor_type_dict[key]} -"
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

    def _remove_sensor_of_system(self):
        print("Running - Remove Sensor of System...")

        self._get_validated_input(prompt=f"Sensor ID to delete:): ",min_value= 1, max_value= len())
        input("Press Enter to return to the menu.")

    def _change_threshold_value(self):
        print("Running - Change Threshold Value...")
        input("Press Enter to return to the menu.")

    def _exit_program(self):
        print("Exiting program & killing all processes. Goodbye!")

        for p in processes:  # Kill all processes
            p.terminate()
        exit()

    def main_menu(self):
        """Display the main menu and handle user input."""
        # --------------- start Servers ---------------
        # start Sensor Server
        self.start_new_subprocess(script="_01_com_manager/sensor_server_socket.py")

        # start loop
        while True:
            self.clear_console()
            print("=== Main Menu ===")
            for idx, (option_text, _) in enumerate(self.menu_options, start=1):
                print(f"{idx}. {option_text}")

            choice = input("Select an option: ")

            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.menu_options):
                    self.clear_console()
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
