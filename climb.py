import math
import os
import random
import sys

from datetime import datetime
from time import time

from nearness import Board

def search(board, final_score=None):
  start = time()
  # https://en.wikipedia.org/wiki/Rule_of_three_(statistics)
  # We want a 99.5% confidence level that the probability is 1e-4:
  max_attempts = int(5.3 * 1e4)
  # We are talking about the probability to find a lower score given
  # that we didn't find any in the first $max_attempts attempts.

  num_pairs = len(board.all_pairs)
  index = 0

  random.shuffle(board.all_pairs)
  while True:
    if final_score and board.rel_score >= final_score:
      return

    next_swap = None
    next_score = board.score

    max_score = 0
    max_swap = None

    attempt = 0
    index %= num_pairs
    for index in range(index, index + num_pairs):
      swap = board.all_pairs[index % num_pairs]
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

    if board.score == board.min_score:
      print("")
      print(board)
      print(
        datetime.now(), board.score, "--", board.rel_score,
        "-- time =", round(time() - start, 2),
      )

if __name__ == "__main__":
  try:
    if len(sys.argv) != 2:
      print("Usage: python climb.py size")
      exit()

    size = int(sys.argv[1])

    board = Board(size)
    if "MEASURE" in os.environ:
      final_score = float(os.environ["MEASURE"])
      search(board, final_score)
    else:
      search(board)
  except:
    pass
