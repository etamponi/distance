import math
import random
import sys

from datetime import datetime
from time import time

from nearness import Board

def search(board):
  alpha = 0.9995

  temp = None
  init_steps = 0
  increase = 0
  board.best_time = math.inf
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
      print(board)
      print(board.score, "--", board.rel_score, "--", temp, "--", datetime.now())
      print("")
      board.best_time = time()

    # Let's say that it is reasonable to consider ourselves stuck if we didn't find
    # any new better score within the time to do 30 "worst case steps".
    # But wait at least 10 seconds.
    if time() - board.best_time > max(10, 30 * len(board.all_pairs) * board.swap_time):
      temp = None
      init_steps = 0
      increase = 0
      board.best_time = math.inf

if __name__ == "__main__":
  start = time()
  try:
    if len(sys.argv) != 2:
      print("Usage: python sa.py size")
      exit()

    size = int(sys.argv[1])

    board = Board(size)
    search(board)
  except:
    print("")
    print("best found in:", int(board.best_time - start), "seconds")
    print("total running time:", int(time() - start), "seconds")
    pass
