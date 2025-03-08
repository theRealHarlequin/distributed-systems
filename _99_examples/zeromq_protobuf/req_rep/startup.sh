. ../venv/bin/activate

python server.py &
PID1=$!

sleep 2

python client.py
kill $PID1
