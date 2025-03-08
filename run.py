import logging
import subprocess
import time
import os
from logger import Logger

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
log = Logger()

_scripts = ["client_resp.py", "server_req.py"]
_chapter = "_00_getting_started"
_folder = "_00_req_resp"
processes = []
log.log(msg="init_env", level=logging.INFO)

# Start all scripts
for script in _scripts:
    script_path = os.path.join(current_dir, _chapter, _folder, script)  # Ensure correct path

    # Pass the script name to the subprocess via environment variable
    env = os.environ.copy()
    env["SCRIPT_NAME"] = script  # Set the SCRIPT_NAME environment variable

    p = subprocess.Popen(["python", script_path], env=env)
    log.log(msg=f"start_process of {script} at {script_path}", level=logging.INFO)
    processes.append(p)

# Wait for 3 seconds
time.sleep(3)

# Kill all processes
for p in processes:
    p.terminate()
