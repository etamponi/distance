import math
import os
import random
import sys

from datetime import datetime
from time import time

from nearness import Board

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

  temp = 0
  final_temp = math.inf
  while True:
    if temp is not None and (temp < final_temp):
      random.shuffle(board.all_pairs)
      run += 1

      init_temp = None
      final_temp = None
      increases = []

      temp = None
      step = 0

    if final_score and board.rel_score >= final_score:
      return

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
      temp = init_temp * math.pow(alpha, step) * (1 + (board.score - board.min_score) / board.score)
    elif len(increases) >= 1000:
      avg_increase = sum(increases) / len(increases)
      temp = init_temp = - avg_increase / math.log(0.5)
      # at every run , final_temp will get smaller
      final_temp = - avg_increase / (run * math.log(final_p(0.00005, num_pairs)))
      step = 0
      if debug:
        print("\n\n\ninit_temp =", init_temp, "final_temp =", final_temp, "\n\n\n")

    if board.score == board.min_score:
      is_best = True
      print("")
      print(board)

    if is_best or (debug and step % 500 == 1):
      print(
        datetime.now(), board.score, "--", board.rel_score,
        "-- temp =", round(temp or -1, 2),
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

    if "MEASURE" in os.environ:
      final_score = float(os.environ["MEASURE"])
      search(size, final_score, debug=True)
    else:
      search(size, debug=True)
  except:
    pass
