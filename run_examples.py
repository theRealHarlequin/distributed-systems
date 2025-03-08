import logging
import subprocess
import time
import os
from logger import Logger

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
log = Logger()

_scripts = ["proxy.py", "pub.py", "sub.py"]
_chapter = "_99_examples"
_area = "zeromq_protobuf"
_folder = "pub_sub_proxy"
processes = []
log.log(msg="init_env", level=logging.INFO)

# Start all scripts
for script in _scripts:
    script_path = os.path.join(current_dir, _chapter, _area, _folder, script)  # Ensure correct path

    p = subprocess.Popen(["python", script_path])
    log.log(msg=f"start_process of {script} at {script_path}", level=logging.INFO)
    processes.append(p)

# Wait for 3 seconds
time.sleep(3)

# Kill all processes
for p in processes:
    p.terminate()
