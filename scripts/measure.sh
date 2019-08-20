#!/bin/bash

s=$1
m=$2
n=$3
PID=$$

trap 'kill -TERM -$PID; exit' INT

rm -f measure.out
for i in $(seq 1 $n); do
    MEASURE=$m pypy3 -u sa.py $s | tee -a measure.out
done
