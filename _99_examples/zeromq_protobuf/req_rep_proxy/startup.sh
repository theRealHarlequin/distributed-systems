. ../venv/bin/activate

PIDS=""

python proxy.py &
PIDP=$!

python server.py 1 &
PIDS1=$!

python server.py 2 &
PIDS2=$!

python client.py 1 2 &
PIDC1=$!

python client.py 2 2 &
PIDC2=$!

wait -f $PIDC1 $PIDC2
kill $PIDS1 $PIDS2
kill $PIDP
