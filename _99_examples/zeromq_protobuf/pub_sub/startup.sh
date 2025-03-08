. ../venv/bin/activate

python sub.py 1 1 &
PIDS1=$!

sleep 1

python pub.py 1 &
PIDP1=$!

wait -f $PIDP1
kill $PIDS1
