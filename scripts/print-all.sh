#!/bin/bash

board() {
  size=$1
  grep -B $size "BEST" $size.out | tail -n $((size + 1)) | head -n $size
}

for i in `seq 9 29`; do
  echo "$(board $i);"
done
board 30
