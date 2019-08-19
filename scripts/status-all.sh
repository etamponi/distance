#!/bin/bash

pushd() {
  command pushd "$@" > /dev/null
}

popd() {
  command popd "$@" > /dev/null
}

status() {
  size=$1
  dir=$2
  line=$(grep "BEST" $size.out | tail -n 1)
  date=$(echo $line | awk '{ print $1, $2 }' | awk -F. '{ print $1 }')
  score=$(echo $line | awk '{ print $5 }')

  echo -n "$size: $date  $score"

  if [ ! -z $dir ]; then
    cd $dir
    prev_score=$(status $size | awk '{ print $4 }')
    cd ..
    if (( $(echo "$score >= ${prev_score:0}" | bc -l) )); then
      echo "  $prev_score BETTER"
    else
      echo "  $prev_score"
    fi
  else
    echo ""
  fi
}

for i in `seq 11 30`; do
  status $i $1
done
