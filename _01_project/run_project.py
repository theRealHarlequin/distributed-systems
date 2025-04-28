import logging
import subprocess
import time
import os
from logger import Logger

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
log = Logger()
central_log_path = log.get_log_file_path()

_scripts = [f"_03_data_output\\console_table.py"]
processes = []

log.log(msg="init_env", level=logging.INFO)
run_in_new_console = True

# Start all scripts
for script in _scripts:
    script_path = os.path.join(current_dir, script)  # Ensure correct path

    if run_in_new_console:
        p = subprocess.Popen(["python", script_path, central_log_path],
                             creationflags=subprocess.CREATE_NEW_CONSOLE )
    else:
        p = subprocess.Popen(["python", script_path, central_log_path])

    log.log(msg=f"start_process of {script} at {script_path}", level=logging.INFO)
    processes.append(p)

# Wait for 15 seconds
time.sleep(1000)


# Kill all processes
for p in processes:
    p.terminate()
