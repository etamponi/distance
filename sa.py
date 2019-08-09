import math
import random
import sys

from datetime import datetime
from time import time

from nearness import Board

def search(board):
  start = time()
  alpha = 0.9995
  min_score_ever = math.inf

  temp = None
  init_steps = 0
  increase = 0
  best_time = math.inf
  board.min_score = math.inf
  stuckness = 1
  while True:
    random.shuffle(board.all_pairs)
    selected = None
    for swap in board.all_pairs:
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

    if temp:
      temp *= alpha
    elif init_steps >= 1000:
      temp = - increase / (init_steps * math.log(0.5))

    # Make sure we don't visit this state anymore
    board.skip()

    if selected:
      board.swap(*selected)
    else:
      board.shuffle(1)

    if temp and board.score == board.min_score:
      best_time = time()
      if board.score < min_score_ever:
        min_score_ever = board.score
        print("")
        print(board)
        print(datetime.now(), board.score, "--", board.rel_score, "-- temp =", round(temp, 2), "-- time =", round(best_time - start, 2))

    # Let's say that it is reasonable to consider ourselves stuck if we didn't find
    # any new better score within the time to do stuckness * 20 "worst case steps".
    # But wait at least 10 seconds.
    if time() - best_time > max(10, stuckness * 20 * len(board.all_pairs) * board.swap_time):
      temp = None
      init_steps = 0
      increase = 0
      best_time = math.inf
      board.min_score = math.inf
      stuckness += 1

if __name__ == "__main__":
  try:
    if len(sys.argv) != 2:
      print("Usage: python sa.py size")
      exit()

    size = int(sys.argv[1])

    board = Board(size)
    search(board)
  except:
    pass
