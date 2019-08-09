import math
import random
import sys

from datetime import datetime
from time import time

from nearness import Board

def search(board, absolute_min_score):
  board.best_time = math.inf
  alpha = 0.9995

  temp = None
  init_steps = 0
  increase = 0
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

    if selected:
      board.swap(*selected)
    else:
      # If we did not select anything, then we exhausted all possible
      # neighbors of the current state without finding a better state.
      # So we are safe skipping this state now. Then we shuffle by one,
      # which is a shortcut, as a random swap is the only way out from
      # here anyway.
      board.skip()
      board.shuffle(1)

    if temp and board.score == board.min_score:
      if board.score < absolute_min_score:
        print(board)
        print(board.score, "--", board.rel_score, "--", temp, "--", datetime.now())
        print("")
        absolute_min_score = board.score
      board.best_time = time()

    # Let's say that it is reasonable to consider ourselves stuck if we didn't find
    # any new better score within the time to do 30 "worst case steps"
    # But wait at least 60 seconds
    if time() - board.best_time > max(60, 30 * len(board.all_pairs) * board.swap_time):
      return absolute_min_score

if __name__ == "__main__":
  start = time()
  try:
    if len(sys.argv) != 2:
      print("Usage: python sa.py size")
      exit()

    size = int(sys.argv[1])

    # Reset search
    absolute_min_score = math.inf
    while True:
      board = Board(size)
      absolute_min_score = search(board, absolute_min_score)
  except:
    print("")
    print("best found in:", int(board.best_time - start), "seconds")
    print("total running time:", int(time() - start), "seconds")
    pass
