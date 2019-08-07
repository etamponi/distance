import math
import random
import sys

from datetime import datetime
from time import time

from nearness import Board

BEST_GRID_TIME = 0

def search(board, max_attempts_pct):
  global BEST_GRID_TIME

  max_attempts = int((max_attempts_pct / 100) * len(board.all_pairs))

  min_score = board.score

  while True:
    next_swap = None
    next_score = board.score

    max_score = 0
    max_swap = None

    random.shuffle(board.all_pairs)
    attempt = 0
    for swap in board.all_pairs:
      if board.peek_skipped(*swap):
        continue

      attempt += 1
      if next_swap and attempt > max_attempts:
        break

      peek_score = board.cached_peek_swap(*swap)

      if peek_score < next_score:
        next_swap = swap
        next_score = peek_score

      if peek_score > max_score:
        max_swap = swap
        max_score = peek_score

    if next_swap:
      board.swap(*next_swap)
    elif max_swap:
      board.skip()
      board.swap(*max_swap)
      continue
    else:
      break

    if board.score < min_score:
      print(board)
      print(board.score, "---", datetime.now())
      print("")
      min_score = board.score
      BEST_GRID_TIME = time()

if __name__ == "__main__":
  start = time()
  try:
    if len(sys.argv) != 3:
      print("Usage: python climb.py size max_attempts_exp")
      exit()

    size = int(sys.argv[1])
    max_attempts_pct = int(sys.argv[2])

    board = Board(size)
    search(board, max_attempts_pct)
  except:
    print("")
    print("best found in:", int(BEST_GRID_TIME - start), "seconds")
    print("total running time:", int(time() - start), "seconds")
    pass
