import itertools
import math
import numpy as np
import random
import sys
from datetime import datetime
from tabulate import tabulate
from time import time

def grouplen(sequence, chunk_size):
  return zip(*[iter(sequence)] * chunk_size)

class Board(object):

  BOUNDS = [
    0,

    0,
    10,
    72,
    816,
    3800,
    16_902,
    52_528,
    155_840,
    381_672,
    902_550,

    1_883_244,
    3_813_912,
    7_103_408,
    12_958_148,
    22_225_500,
    37_474_816,
    60_291_180,
    95_730_984,
    146_469_252,
    221_736_200,

    325_763_172,
    474_261_920,
    673_706_892,
    949_783_680,
    1_311_600_000,
    1_799_572_164,
    2_425_939_956,
    3_252_444_776,
    4_294_801_980,
    5_643_997_650,
  ]

  def __init__(self, size, cells=None):
    self.size = size

    # orig_dists is always the same
    self.cells = []
    for row in range(size):
      for col in range(size):
        self.cells.append((row, col))
    self.orig_dists = self.calc_dists()

    if cells:
      self.cells = cells
      self.dists = self.calc_dists()
    else:
      self.dists = np.copy(self.orig_dists)

    self.scores = self.dists * self.orig_dists
    self.scores_sum = np.sum(self.scores)

  def calc_dists(self):
    size = self.size
    cells = self.cells
    dists = np.zeros((size*size, size*size), dtype="u4")
    for i in range(size*size):
      for j in range(size*size):
        a = cells[i]
        b = cells[j]
        dists[i][j] = self.cell_dist(a, b)
    return dists

  def cell_dist(self, a, b):
    return sum(d**2 for d in (min(abs(ap - bp), self.size - abs(ap - bp)) for (ap, bp) in zip(a, b)))

  def score(self):
    return self.scores_sum / 2 - Board.BOUNDS[self.size]

  def __repr__(self):
    board = grouplen(self.cells, self.size)
    rows = ["({})".format(", ".join([self.cell_repr(cell) for cell in row])) for row in board]
    return ",\n".join(rows)

  def cell_repr(self, cell):
    A = ord('A')
    Z = ord('Z')
    return "{}{}".format(*(chr(v + A) if v + A <= Z else v + A - Z for v in cell))

  def swap_already_seen(self, index_a, index_b, seen):
    self.cells[index_b], self.cells[index_a] = self.cells[index_a], self.cells[index_b]
    skip = str(self.cells) in seen
    self.cells[index_b], self.cells[index_a] = self.cells[index_a], self.cells[index_b]
    return skip

  def swap_preview(self, index_a, index_b, seen=None):
    if seen and self.swap_already_seen(index_a, index_b, seen):
      return None, True

    self.swap(index_a, index_b)
    score = self.score()
    self.swap(index_a, index_b)
    return score, False

  def swap(self, index_a, index_b):
    self.cells[index_b], self.cells[index_a] = self.cells[index_a], self.cells[index_b]
    
    self.dists[[index_b, index_a], :] = self.dists[[index_a, index_b], :]
    self.dists[:, [index_b, index_a]] = self.dists[:, [index_a, index_b]]

    # Refresh scores
    self.scores_sum -= np.sum(self.scores[index_a, :])
    self.scores_sum -= np.sum(self.scores[:, index_a])
    self.scores_sum -= np.sum(self.scores[index_b, :])
    self.scores_sum -= np.sum(self.scores[:, index_b])

    self.scores[index_a, :] = self.dists[index_a, :] * self.orig_dists[index_a, :]
    self.scores[:, index_a] = self.dists[:, index_a] * self.orig_dists[:, index_a]
    self.scores[index_b, :] = self.dists[index_b, :] * self.orig_dists[index_b, :]
    self.scores[:, index_b] = self.dists[:, index_b] * self.orig_dists[:, index_b]

    self.scores_sum += np.sum(self.scores[index_a, :])
    self.scores_sum += np.sum(self.scores[:, index_a])
    self.scores_sum += np.sum(self.scores[index_b, :])
    self.scores_sum += np.sum(self.scores[:, index_b])

def greedy_search(board, steps):
  min_score = board.score()
  min_swap = None
  for _ in range(steps):
    for index_a in range(board.size * board.size - 1):
      for index_b in range(index_a + 1, board.size*board.size):
        score, _ = board.swap_preview(index_a, index_b)
        if score < min_score:
          min_score = score
          min_swap = (index_a, index_b)
    if min_swap:
      board.swap(*min_swap)
      print(board)
      print(board.score())
      print("-----------")
      min_swap = None
    else:
      break

def random_pair(board):
  index_a = random.randrange(board.size*board.size - 1)
  index_b = random.randrange(index_a + 1, board.size*board.size)
  return (index_a, index_b)

def random_swaps(board, swaps):
  for _ in range(swaps):
    index_a, index_b = random_pair(board)
    board.swap(index_a, index_b)

def almost_greedy_search(board):
  curr_score = min_score = board.score()
  seen = set()
  while True:
    min_swap = None
    curr_max_score = 0
    max_swap = None
    for swap in itertools.combinations(range(board.size*board.size), 2):
      score, skip = board.swap_preview(*swap, seen)
      if skip:
        continue

      if score < curr_score:
        min_swap = swap
        curr_score = score

      if score > curr_max_score:
        max_swap = swap
        curr_max_score = score

    if not min_swap and not max_swap:
      break

    swap = min_swap or max_swap
    board.swap(*swap)
    seen.add(str(board.cells))

    curr_score = board.score()

    if curr_score < min_score:
      min_score = curr_score
      # print(tabulate(board.dists))
      print(datetime.now())
      print(board)
      print(curr_score)
      print("------------")

def random_search(board):
  attempts = board.size**3
  curr_score = min_score = board.score()
  seen = set()

  pairs = [*itertools.combinations(range(board.size*board.size), 2)]

  while True:
    min_swap = None
    curr_max_score = 0
    max_swap = None
    random.shuffle(pairs)
    attempt = 0
    for swap in pairs:
      score, skip = board.swap_preview(*swap, seen)
      if skip:
        continue

      if score < curr_score:
        min_swap = swap
        curr_score = score

      if score > curr_max_score:
        max_swap = swap
        curr_max_score = score

      attempt += 1
      if attempt > attempts:
        break

    if not min_swap and not max_swap:
      break

    swap = min_swap or max_swap
    board.swap(*swap)
    seen.add(str(board.cells))

    curr_score = board.score()

    if curr_score < min_score:
      min_score = curr_score
      # print(tabulate(board.dists))
      print(datetime.now())
      print(board)
      print(curr_score)
      print("------------")

def dfs(board, max_attempts=None):
  curr_score = min_score = board.score()
  if max_attempts is None:
    max_attempts = math.inf

  path = [{ "swap": None, "next": {} }]
  seen = set()

  swaps = [*itertools.combinations(range(board.size*board.size), 2)]

  while True:
    min_swap = None
    attempt = 0
    random.shuffle(swaps)
    for swap in swaps:
      if min_swap and attempt > max_attempts:
        break
      attempt += 1

      if swap not in path[-1]["next"]:
        path[-1]["next"][swap] = board.swap_preview(*swap, seen)

      score, skip = path[-1]["next"][swap]
      if skip or board.swap_already_seen(*swap, seen):
        path[-1]["next"][swap] = None, True
        continue
      
      if score < curr_score:
        min_swap = swap
        curr_score = score

    # Local minimum!
    if not min_swap:
      # We can't go up!
      if path[-1]["swap"] is None:
        print("CAN'T GO UP!")
        break
      # print("GOING UP!")
      seen.add(str(board.cells))
      # Go up in the path
      board.swap(*path.pop()["swap"])
    else:
      board.swap(*min_swap)
      path.append({"swap": min_swap, "next": {}})

    curr_score = board.score()
    if curr_score < min_score:
      min_score = curr_score
      # print(tabulate(board.dists))
      print(datetime.now())
      print(board)
      print(curr_score)
      print("------------")

def simulated_annealing(board, temp=None):
  curr_score = min_score = board.score()
  if temp is None:
    temp = curr_score * 0.1

  seen = set()
  swaps = [*itertools.combinations(range(board.size*board.size), 2)]

  while True:
    swap = swaps[random.randrange(len(swaps))]
    score, skip = board.swap_preview(*swap, seen)

    if skip:
      continue

    # update temperature
    temp = max(temp * 0.9995, curr_score * 0.00001)

    if score > curr_score:
      prob = max(0.01, math.exp(-(score - curr_score) / temp))
      # print(prob)
      if random.random() > prob:
        continue

    board.swap(*swap)
    seen.add(str(board.cells))
    curr_score = board.score()
    if curr_score < min_score:
      min_score = curr_score
      # print(tabulate(board.dists))
      print(datetime.now())
      print(board)
      print(curr_score)
      print("------------")

if __name__ == "__main__":
  size = int(sys.argv[1])
  board = Board(size)
  
  # print(tabulate(board.dists))
  # print([*board.dists[0, :]])
  # print([*board.dists[:, 0]])
  # print([*reversed(board.dists[-1, :])])
  # print([*reversed(board.dists[:, -1])])

  # print(tabulate(board.dists))
  # print(board.score())
  # board.swap(4, 6)
  # print(tabulate(board.dists))
  # print(board.score())

  # random_swaps(board, size * size * size)
  # print(board)
  # print(board.score())
  # print("------------")
  random_search(board)
  # almost_greedy_search(board)
  # print(board)
  # print(board.score())
