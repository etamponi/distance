import math
import os
import random
import sys

from datetime import datetime
from time import time

from on import Board

# the probability that at least one element will be picked among n elements,
# where p is the probability of picking one of them.
def final_p(p, n):
  return 1 - (1 - p)**(1 / n)

def search(size, final_score=None, debug=None):
  alpha = 0.9995
  start = time()

  board = Board(size)
  num_pairs = len(board.all_pairs)
  index = 0
  run = 0
  keep_warm = 0
  min_score_ever = math.inf

  # set temp and final_temp in order to initialize the cycle at line 34
  temp = 0
  final_temp = math.inf
  while True:
    if final_score and board.rel_score >= final_score:
      return

    if temp is not None and (temp < final_temp):
      random.shuffle(board.all_pairs)
      run += 1

      init_temp = None
      final_temp = None
      increases = []

      temp = None
      step = 0

      board.min_score = math.inf

    selected = None
    index %= num_pairs
    is_best = False
    for index in range(index + 1, index + num_pairs):
      swap = board.all_pairs[index % num_pairs]
      if board.peek_skipped(*swap):
        continue

      peek_score = board.peek_swap(*swap)

      if peek_score < board.score:
        selected = swap
        break

      if not init_temp:
        # when initializing, accept all increases and log
        increases.append(peek_score - board.score)
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

    if init_temp:
      step += 1
      if keep_warm <= 0:
        temp = init_temp * math.pow(alpha, step) * (1 + (board.score - board.min_score) / board.score)
      else:
        keep_warm -= 1
    elif len(increases) >= 1000:
      avg_increase = sum(increases) / len(increases)
      # at every run, init_temp gets larger and final_temp gets smaller
      temp = init_temp = - avg_increase / math.log(min(0.9, 0.5 + 0.02 * run))
      final_temp = - avg_increase / (run * math.log(final_p(0.0005, num_pairs)))
      step = 0
      if debug:
        print("\n\n\ninit_temp =", init_temp, "final_temp =", final_temp, "\n\n\n")

    if board.score == board.min_score:
      keep_warm = run * 100
      if board.score < min_score_ever:
        min_score_ever = board.score
        is_best = True
        print("")
        print(board)

    if is_best or (debug and step % 500 == 1):
      print(
        datetime.now(), board.score, "--", board.rel_score,
        "-- time =", round(time() - start, 2),
        "-- temp =", round(temp or -1, 2),
        "-- warm =", keep_warm,
        "-- step =", step,
        "-- run =", run,
        "BEST" if is_best else "",
      )

if __name__ == "__main__":
  try:
    if len(sys.argv) != 2:
      print("Usage: pypy3 sa.py size")
      exit()

    size = int(sys.argv[1])

    if "MEASURE" in os.environ:
      final_score = float(os.environ["MEASURE"])
      search(size, final_score, debug=True)
    else:
      search(size, debug=True)
  except:
    pass
