import math
import random
import sys

from datetime import datetime
from time import time

from nearness import Board

def search(board):
  # https://en.wikipedia.org/wiki/Rule_of_three_(statistics)
  # We want a 99.5% confidence level that the probability is 1e-4:
  max_attempts = 5.3 * 1e4
  # We are talking about the probability to find a lower score given
  # that we didn't find any in the first $max_attempts attempts.

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
      if attempt > max_attempts:
        break

      peek_score = board.peek_swap(*swap)

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
    else:
      break

    if board.score < min_score:
      print(board)
      print(board.score, "--", board.rel_score, "--", board.swap_count, "--", datetime.now())
      print("")
      min_score = board.score
      board.best_time = time()

if __name__ == "__main__":
  start = time()
  try:
    if len(sys.argv) != 2:
      print("Usage: python climb.py size")
      exit()

    size = int(sys.argv[1])

    board = Board(size)
    search(board)
  except:
    print("")
    print("best found in:", int(board.best_time - start), "seconds")
    print("total running time:", int(time() - start), "seconds")
    pass
