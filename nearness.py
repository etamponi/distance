import itertools
import random

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

  138133813,
  203877974,
  286970392,
  409180212,
  560367595,
  776307056,
  1039384551,
  1404826716,
  1843400528,
  2439448486,
]

class Board:

  def __init__(self, size):
    self.size = size
    self.orig = self.initial_distances()
    self.grid = self.initial_grid()

    self.dists = self.initial_distances()
    self.scores = self.prod4(self.dists, self.orig)
    self.score = self.sum4(self.scores) / 2 - BOUNDS[self.size]
    self.rel_score = round(BEST_SCORES[self.size] / self.score, 6)

    self.skipped = set()

    self.all_pairs = list(itertools.combinations(((i, j) for i in range(size) for j in range(size)), 2))

    self.min_score = self.score
    self.swap_count = 0

  def initial_distances(self):
    m = [[[[0 for l in range(self.size)] for k in range(self.size)] for j in range(self.size)] for i in range(self.size)]
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

  def prod4(self, m1, m2):
    m = [[[[0 for l in range(self.size)] for k in range(self.size)] for j in range(self.size)] for i in range(self.size)]
    for i in range(self.size):
      for j in range(self.size):
        for k in range(self.size):
          for l in range(self.size):
            m[i][j][k][l] = m1[i][j][k][l] * m2[i][j][k][l]
    return m

  def sum4(self, m):
    s = 0
    for i in range(self.size):
      for j in range(self.size):
        for k in range(self.size):
          for l in range(self.size):
            s += m[i][j][k][l]
    return s

  def swap2(self, d, a, b):
    (i0, j0), (i1, j1) = a, b
    for k in range(self.size):
      for l in range(self.size):
        d[i0][j0][k][l], d[i1][j1][k][l] = d[i1][j1][k][l], d[i0][j0][k][l]
    for k in range(self.size):
      for l in range(self.size):
        d[k][l][i0][j0], d[k][l][i1][j1] = d[k][l][i1][j1], d[k][l][i0][j0]

  def sum2(self, m, a):
    i, j = a
    s = 0
    for k in range(self.size):
      for l in range(self.size):
        s += m[i][j][k][l] + m[k][l][i][j]
    return s

  def prod2(self, m, m1, m2, a):
    i, j = a
    for k in range(self.size):
      for l in range(self.size):
        m[i][j][k][l] = m1[i][j][k][l] * m2[i][j][k][l]
        m[k][l][i][j] = m1[k][l][i][j] * m2[k][l][i][j]

  def swap(self, a, b):
    start = time()

    self.swap2(self.dists, a, b)

    self.score = (self.score + BOUNDS[self.size]) * 2

    self.score -= self.sum2(self.scores, a) + self.sum2(self.scores, b)

    self.prod2(self.scores, self.dists, self.orig, a)
    self.prod2(self.scores, self.dists, self.orig, b)

    self.score += self.sum2(self.scores, a) + self.sum2(self.scores, b)

    self.score = self.score / 2 - BOUNDS[self.size]
    self.rel_score = round(BEST_SCORES[self.size] / self.score, 6)
    if self.score < self.min_score:
      self.min_score = self.score

    self.swap_grid(a, b)

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
    self.skipped.add(tuple(itertools.chain(*self.grid)))

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
