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
  best_time = math.inf

  temp = 0  
  while True:
    if 'MEASURE' in os.environ and board.rel_score == 1:
      return

    if temp is not None and temp < 1:
      init_temp = None
      init_steps = 0
      increase = 0
      temp = None
      step = 0
      random.shuffle(board.all_pairs)

    selected = None
    index %= num_pairs
    for index in range(index, index + num_pairs):
      swap = board.all_pairs[index % num_pairs]
      if board.peek_skipped(*swap):
        continue

      peek_score = board.peek_swap(*swap)

      if peek_score < board.score:
        selected = swap
        break

      if not temp:
        # accept all increases and log
        increase += (peek_score - board.score)
        init_steps += 1
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
    elif init_steps >= 1000:
      temp = init_temp = - increase / (init_steps * math.log(0.5))

    if board.score == board.min_score:
      best_time = time()
      print("")
      print(board)
      print(datetime.now(), board.score, "--", board.rel_score, "-- temp =", round(temp or 0, 2), "-- time =", round(best_time - start, 2))

if __name__ == "__main__":
  try:
    if len(sys.argv) != 2:
      print("Usage: python sa.py size")
      exit()

    size = int(sys.argv[1])

    search(size)
  except:
    pass
