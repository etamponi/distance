import math
import os
import random
import sys

from datetime import datetime
from time import time

from nearness import Board

def search(size):
  board = Board(size)
  alpha = 0.9995

  start = time()
  num_pairs = len(board.all_pairs)
  index = 0
  run = 0

  temp = 0
  while True:
    if 'MEASURE' in os.environ and board.rel_score == 1:
      return

    if temp is not None and (temp < 10):
      init_temp = None
      increase = 0
      temp = None
      step = 0
      random.shuffle(board.all_pairs)
      run += 1

    selected = None
    index %= num_pairs
    is_best = False
    for index in range(index, index + num_pairs):
      swap = board.all_pairs[index % num_pairs]
      if board.peek_skipped(*swap):
        continue

      peek_score = board.peek_swap(*swap)

      if peek_score < board.score:
        selected = swap
        break

      if not temp:
        # when initializing, accept all increases and log
        increase += (peek_score - board.score)
        step += 1
        selected = swap
        break

      pick_prob = math.exp(-(peek_score - board.score) / temp)
      if random.random() < pick_prob:
        selected = swap
        break

    # Make sure we don't visit this state anymore
    board.skip()

    if selected:
      board.swap(*selected)
    else:
      board.shuffle(1)

    if temp:
      step += 1
      temp = init_temp * math.pow(alpha, step) * (1 + (board.score - board.min_score) / board.score)
    elif step >= 1000:
      temp = init_temp = - increase / (step * math.log(0.5))
      step = 0

    if board.score == board.min_score:
      is_best = True

    if is_best or step % 500 == 1:
      print("")
      print(board)
      print(
        datetime.now(), board.score, "--", board.rel_score,
        "-- temp =", round(temp or 0, 2),
        "-- time =", round(time() - start, 2),
        "-- step =", step,
        "-- run =", run,
        "BEST" if is_best else "",
      )

if __name__ == "__main__":
  try:
    if len(sys.argv) != 2:
      print("Usage: python sa.py size")
      exit()

    size = int(sys.argv[1])

    search(size)
  except:
    pass
