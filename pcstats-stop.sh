#!/bin/bash
if [ ! -z "$(pgrep -f pcstats.py)" ]
then
	let pid=$(pgrep -f pcstats.py)
	echo "piPCStats is stopped (kill)."
	sudo -E kill -9 $pid
	if [ ! -z "$(pgrep -f pcstats.py)" ]
	then
        	let pid=$(pgrep -f pcstats.py)
	        echo "piPCStats is stopped (kill)."
        	sudo -E kill -9 $pid
	fi

else
	echo "piPCStats is not running."
fi
