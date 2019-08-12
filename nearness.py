import itertools
import numpy as np
import random

from lru import LRU
from time import time

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

BEST_SCORES = [
  0,
  0,
  0,
  0,
  0,
  0,

  5526,
  17779,
  57152,
  144459,
  362950,

  740798,
  1585264,
  2888120,
  5457848,
  9164700,
  15891088,
  25152826,
  40901354,
  61784724,
  95115180,

  138133955,
  203887948,
  286970392,
  409180212,
  560367595,
  776307056,
  1039464019,
  1404894470,
  1843400528,
  2439463054,
]

class Board(object):

  def __init__(self, size):
    self.size = size
    self.orig = self.initial_distances()
    self.grid = self.initial_grid()

    self.dists = np.array(self.orig)
    self.scores = self.dists * self.orig
    self.score = np.sum(self.scores) / 2 - BOUNDS[self.size]
    self.rel_score = round(BEST_SCORES[self.size] / self.score, 4)

    self.skipped = LRU(1500000)

    self.all_pairs = list(itertools.combinations(((i, j) for i in range(size) for j in range(size)), 2))

    self.min_score = self.score
    self.swap_count = 0

  def initial_distances(self):
    m = np.zeros((self.size, self.size, self.size, self.size))
    for i in range(self.size):
      for j in range(self.size):
        for k in range(self.size):
          for l in range(self.size):
            xdiff = min(abs(i - k), self.size - abs(i - k))
            ydiff = min(abs(j - l), self.size - abs(j - l))
            m[i][j][k][l] = xdiff*xdiff + ydiff*ydiff
    return m

  def initial_grid(self):
    return [[(i, j) for j in range(self.size)] for i in range(self.size)]

  def swap(self, a, b):
    start = time()
    self.swap_grid(a, b)

    m = self.dists
    w = m.swapaxes(0, 2).swapaxes(1, 3)
    m[(a[0], b[0]), (a[1], b[1]), :, :] = m[(b[0], a[0]), (b[1], a[1]), :, :]
    w[(a[0], b[0]), (a[1], b[1]), :, :] = w[(b[0], a[0]), (b[1], a[1]), :, :]

    self.score = (self.score + BOUNDS[self.size]) * 2

    self.score -= np.sum([
      self.scores[a[0], a[1], :, :],
      self.scores[b[0], b[1], :, :],
      self.scores[:, :, a[0], a[1]],
      self.scores[:, :, b[0], b[1]],
    ])

    self.scores[a[0], a[1], :, :] = m[a[0], a[1], :, :] * self.orig[a[0], a[1], :, :]
    self.scores[b[0], b[1], :, :] = m[b[0], b[1], :, :] * self.orig[b[0], b[1], :, :]
    self.scores[:, :, a[0], a[1]] = m[:, :, a[0], a[1]] * self.orig[:, :, a[0], a[1]]
    self.scores[:, :, b[0], b[1]] = m[:, :, b[0], b[1]] * self.orig[:, :, b[0], b[1]]

    self.score += np.sum([
      self.scores[a[0], a[1], :, :],
      self.scores[b[0], b[1], :, :],
      self.scores[:, :, a[0], a[1]],
      self.scores[:, :, b[0], b[1]],
    ])

    self.score = self.score / 2 - BOUNDS[self.size]
    self.rel_score = round(BEST_SCORES[self.size] / self.score, 4)
    if self.score < self.min_score:
      self.min_score = self.score

    self.swap_count += 1

    self.swap_time = time() - start

    return self.score

  def swap_grid(self, a, b):
    self.grid[a[0]][a[1]], self.grid[b[0]][b[1]] = self.grid[b[0]][b[1]], self.grid[a[0]][a[1]]

  def peek_swap(self, a, b):
    self.swap_count -= 2
    peek_score = self.swap(a, b)
    self.swap(a, b)
    return peek_score

  def peek_skipped(self, a, b):
    self.swap_grid(a, b)
    skip = tuple(itertools.chain(*self.grid)) in self.skipped
    self.swap_grid(a, b)
    return skip

  def skip(self):
    self.skipped[tuple(itertools.chain(*self.grid))] = True

  def shuffle(self, swap_num):
    while swap_num > 0:
      swap = random.choice(self.all_pairs)
      if not self.peek_skipped(*swap):
        swap_num -= 1
      self.swap(*swap)
    return self.score

  def __repr__(self):
    return ",\n".join(["({})".format(", ".join([self.cell_repr(cell) for cell in row])) for row in self.grid])

  def cell_repr(self, cell):
    A = ord('A')
    Z = ord('Z')
    return "{}{}".format(*(chr(int(v) + A) if int(v) + A <= Z else int(v) + A - Z for v in cell))
