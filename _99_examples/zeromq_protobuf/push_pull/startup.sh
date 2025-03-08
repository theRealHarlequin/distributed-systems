. ../venv/bin/activate

PIDW=""
for i in $(seq 1 10); do
	python worker.py $i &
	PIDW="$PIDW $!"
done

python sink.py &
PIDX=$!

sleep 5

python sender.py 10 1000 &
PIDS=$!

wait -f $PIDX

kill $PIDW

