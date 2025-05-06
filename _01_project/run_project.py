import logging
import subprocess
import time
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

        if run_in_new_console:
            p = subprocess.Popen(["python", script_path, "--log-dir", self.log_path],
                                 creationflags=subprocess.CREATE_NEW_CONSOLE )
        else:
            p = subprocess.Popen(["python", script_path, self.log_path])

        log.log(msg=f"start_process of {script} at {script_path}", level=logging.INFO)
        processes.append(p)


    def clear_console(self):
        """Clear the console output."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _add_sensor_to_system(self):
        """Example task 1."""
        print("Running - Add Sensor to System...")

        input("Press Enter to return to the menu.")

    def _remove_sensor_of_system(self):
        """Example task 2."""
        print("Running - Remove Sensor of System...")
        input("Press Enter to return to the menu.")

    def _change_threshold_value(self):
        """Example task 3."""
        print("Running - Change Threshold Value...")
        input("Press Enter to return to the menu.")

    def _exit_program(self):
        """Exit the program."""
        print("Exiting program & killing all processes. Goodbye!")

        for p in processes:  # Kill all processes
            p.terminate()
        exit()

    def main_menu(self):
        """Display the main menu and handle user input."""
        ### test prep


        ###
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
