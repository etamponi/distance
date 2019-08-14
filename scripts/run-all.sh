#!/bin/bash

PID=$$

trap 'kill -TERM -$PID; exit' INT

for i in `seq 11 30`; do
  python -u sa.py $i > $i.out &
done

wait
