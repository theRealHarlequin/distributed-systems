import logging
import subprocess
import time
import os
from logger import Logger

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
log = Logger()

_chapter = "_99_examples"
_area = "zeromq_protobuf"

# pub_sub
_scripts = ["pub.py", "sub.py"]
_param = [["1"], ["1", "1"]]
_folder = "pub_sub"

# pub_sub_proxy
#_scripts = ["proxy.py", "pub.py", "sub.py"]
#_param = [["1"], ["1", "1"]]
#_folder = "pub_sub_proxy"


processes = []
log.log(msg="init_env", level=logging.INFO)

# Start all scripts
for i in range(0,len(_scripts) - 1):
    script_path = os.path.join(current_dir, _chapter, _area, _folder, _scripts[i])  # Ensure correct path

    p = subprocess.Popen(["python", script_path] + _param[i])
    log.log(msg=f"start_process of {_scripts[i]} at {script_path}", level=logging.INFO)
    processes.append(p)

# Wait for 3 seconds
time.sleep(3)

# Kill all processes
for p in processes:
    p.terminate()
