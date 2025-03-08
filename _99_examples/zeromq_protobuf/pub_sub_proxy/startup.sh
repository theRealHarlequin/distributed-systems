. ../venv/bin/activate

python proxy.py &
PIDP=$!

python pub.py 1 &
PIDP1=$!

python pub.py 2 &
PIDP2=$!

python sub.py 1 1 &
PIDS1=$!

python sub.py 2 2 &
PIDS2=$!

wait -f $PIDP1 $PIDP2
kill $PIDS1 $PIDS2
kill $PIDP
