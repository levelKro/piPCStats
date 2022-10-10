#!/bin/bash
workdir="$(dirname "$0")"
cd /home/pi/pcstats/pi
DISPLAY=:0 sudo python3 pcstats.py >/home/pi/pcstats/app.log 2>&1 &
