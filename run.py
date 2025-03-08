import subprocess
import time
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

_scripts = ["client_resp.py", "server_req.py"]
_chapter = "_00_getting_started"
_folder = "_00_req_resp"
processes = []

# Start all scripts
for script in _scripts:
    script_path = os.path.join(current_dir, _chapter, _folder, script)  # Ensure correct path
    p = subprocess.Popen(["python", script_path])  # Use "python3" if needed
    processes.append(p)

# Wait for 3 seconds
time.sleep(3)

# Kill all processes
for p in processes:
    p.terminate()

