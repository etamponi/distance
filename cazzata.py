import math
import numpy as np
import random
import sys

from datetime import datetime
from time import time

from nearness import Board

def search(board):
  min_score = board.score

  while True:
    next_swap = None
    next_score = math.inf

    max_score = 0
    max_swap = None

    partial_scores_sum = np.sum(board.scores, axis=(0, 1))
    max_partial = np.max(partial_scores_sum)
    for (pos1, pos2) in board.all_pairs:
      if partial_scores_sum[pos1] < max_partial and partial_scores_sum[pos2] < max_partial:
        continue

      if board.peek_skipped(pos1, pos2):
        continue

      peek_score = board.peek_swap(pos1, pos2)

      if peek_score < next_score:
        next_swap = (pos1, pos2)
        next_score = peek_score

      if peek_score > max_score:
        max_swap = (pos1, pos2)
        max_score = peek_score

    if next_swap:
      board.swap(*next_swap)
    else:
      board.swap(*max_swap)
    board.swap(*next_swap)
    board.skip()

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
      print("Usage: python cazzata.py size")
      exit()

    size = int(sys.argv[1])
    board = Board(size)

    search(board)
  except:
    print("")
    print("best found in:", int(board.best_time - start), "seconds")
    print("total running time:", int(time() - start), "seconds")
    pass
