import itertools
import numpy as np
import random

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

class Cell:
    # Original x, y coordinates
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __repr__(self):
        A = ord('A')
        Z = ord('Z')
        return "{}{}".format(*(chr(int(v) + A) if int(v) + A <= Z else int(v) + A - Z for v in (self.x, self.y)))

class Board:
    def __init__(self, size):
        self.size = size
        self.cells = [ [ Cell(i, j) for j in range(size) ] for i in range(size) ]
        self.dist = np.array([ [self.calc_dist(i0, i) for i in range(size) ] for i0 in range(size) ])
        self.sum_dist_xi = np.array([ [self.calc_sum_dist_xi(x_i0_j0, i) for i in range(size)] for x_i0_j0 in range(size) ])
        self.sum_dist_yi = np.array([ [self.calc_sum_dist_yi(y_i0_j0, i) for i in range(size)] for y_i0_j0 in range(size) ])
        self.sum_dist_xj = np.array([ [self.calc_sum_dist_xj(x_i0_j0, j) for j in range(size)] for x_i0_j0 in range(size) ])
        self.sum_dist_yj = np.array([ [self.calc_sum_dist_yj(y_i0_j0, j) for j in range(size)] for y_i0_j0 in range(size) ])

        self.score_xi = sum(sum(self.calc_score_xi(i, j) for i in range(size)) for j in range(size))
        self.score_yi = sum(sum(self.calc_score_yi(i, j) for i in range(size)) for j in range(size))
        self.score_xj = sum(sum(self.calc_score_xj(i, j) for i in range(size)) for j in range(size))
        self.score_yj = sum(sum(self.calc_score_yj(i, j) for i in range(size)) for j in range(size))

        self.min_score = self.score = self.calc_score()
        self.rel_score = round(BEST_SCORES[self.size] / self.score, 6)

        self.all_pairs = list(itertools.combinations(((i, j) for i in range(size) for j in range(size)), 2))
        self.swap_count = 0
    
    def __repr__(self):
        return ",\n".join(["({})".format(", ".join([str(cell) for cell in row])) for row in self.cells])

    # The following five methods don't need to be optimized for speed.
    # ONLY FOR TEST AND IN THE CONSTRUCTOR -- START
    def calc_dist(self, a, b):
        return min(abs(a - b), self.size - abs(a - b))**2

    def calc_sum_dist_xi(self, x_i0_j0, i):
        return sum(self.dist[x_i0_j0][self.cells[i][j].x] for j in range(self.size))

    def calc_sum_dist_yi(self, y_i0_j0, i):
        return sum(self.dist[y_i0_j0][self.cells[i][j].y] for j in range(self.size))

    def calc_sum_dist_xj(self, x_i0_j0, j):
        return sum(self.dist[x_i0_j0][self.cells[i][j].x] for i in range(self.size))

    def calc_sum_dist_yj(self, y_i0_j0, j):
        return sum(self.dist[y_i0_j0][self.cells[i][j].y] for i in range(self.size))
    # ONLY FOR TEST AND IN THE CONSTRUCTOR -- END

    def calc_score_xi(self, i0, j0):
        x_i0_j0 = self.cells[i0][j0].x
        return np.sum(self.dist[i0, :] * self.sum_dist_xi[x_i0_j0, :])

    def calc_score_yi(self, i0, j0):
        y_i0_j0 = self.cells[i0][j0].y
        return np.sum(self.dist[i0, :] * self.sum_dist_yi[y_i0_j0, :])

    def calc_score_xj(self, i0, j0):
        x_i0_j0 = self.cells[i0][j0].x
        return np.sum(self.dist[j0, :] * self.sum_dist_xj[x_i0_j0, :])

    def calc_score_yj(self, i0, j0):
        y_i0_j0 = self.cells[i0][j0].y
        return np.sum(self.dist[j0, :] * self.sum_dist_yj[y_i0_j0, :])

    def calc_score(self):
        return (self.score_xi + self.score_xj + self.score_yi + self.score_yj) / 2 - BOUNDS[self.size]

    def swap(self, a, b):
        (i0, j0), (i1, j1) = a, b
        self.score_xi -= 2*self.calc_score_xi(i0, j0)
        self.score_xi -= 2*self.calc_score_xi(i1, j1)
        self.score_yi -= 2*self.calc_score_yi(i0, j0)
        self.score_yi -= 2*self.calc_score_yi(i1, j1)
        self.score_xj -= 2*self.calc_score_xj(i0, j0)
        self.score_xj -= 2*self.calc_score_xj(i1, j1)
        self.score_yj -= 2*self.calc_score_yj(i0, j0)
        self.score_yj -= 2*self.calc_score_yj(i1, j1)

        x0, x1 = self.cells[i0][j0].x, self.cells[i1][j1].x
        if x0 != x1:
            self.sum_dist_xi[:, i0] += self.dist[:, x1] - self.dist[:, x0]
            self.sum_dist_xi[:, i1] += self.dist[:, x0] - self.dist[:, x1]

            self.sum_dist_xj[:, j0] += self.dist[:, x1] - self.dist[:, x0]
            self.sum_dist_xj[:, j1] += self.dist[:, x0] - self.dist[:, x1]

        y0, y1 = self.cells[i0][j0].y, self.cells[i1][j1].y
        if y0 != y1:
            self.sum_dist_yi[:, i0] += self.dist[:, y1] - self.dist[:, y0]
            self.sum_dist_yi[:, i1] += self.dist[:, y0] - self.dist[:, y1]

            self.sum_dist_yj[:, j0] += self.dist[:, y1] - self.dist[:, y0]
            self.sum_dist_yj[:, j1] += self.dist[:, y0] - self.dist[:, y1]

        self.cells[i0][j0], self.cells[i1][j1] = self.cells[i1][j1], self.cells[i0][j0]

        self.score_xi += 2*self.calc_score_xi(i0, j0)
        self.score_xi += 2*self.calc_score_xi(i1, j1)
        self.score_yi += 2*self.calc_score_yi(i0, j0)
        self.score_yi += 2*self.calc_score_yi(i1, j1)
        self.score_xj += 2*self.calc_score_xj(i0, j0)
        self.score_xj += 2*self.calc_score_xj(i1, j1)
        self.score_yj += 2*self.calc_score_yj(i0, j0)
        self.score_yj += 2*self.calc_score_yj(i1, j1)

        self.score = self.calc_score()
        self.rel_score = round(BEST_SCORES[self.size] / self.score, 6)
        if self.score < self.min_score:
            self.min_score = self.score
        self.swap_count += 1

        return self.score
    
    def peek_swap(self, a, b):
        self.swap_count -= 2
        peek_score = self.swap(a, b)
        self.swap(a, b)
        return peek_score

    def shuffle(self, swap_num):
        while swap_num > 0:
            (a, b) = random.choice(self.all_pairs)
            if not self.peek_skipped(a, b):
                swap_num -= 1
            self.swap(a, b)
        return self.score

    # no-op, at least for now, because they'd have O(n^2) complexity
    def peek_skipped(self, a, b):
        return False

    def skip(self):
        pass

def matrix(m):
    return "\n".join(" ".join("{: 3d}".format(d) for d in line) for line in m)

if __name__ == "__main__":
    board = Board(4)

    board.swap((0, 1), (2, 3))
    board.swap((3, 2), (1, 0))
    board.swap((2, 0), (3, 1))
    # board.swap((2, 0), (3, 1))
    # board.swap((3, 2), (1, 0))
    # board.swap((0, 1), (2, 3))
    print(board)
    print("")

    print(board.score_xi, board.score_xj, board.score_yi, board.score_yj, board.score)
    print(sum(sum(board.calc_score_xi(i, j) for i in range(board.size)) for j in range(board.size)))
    print(sum(sum(board.calc_score_xj(i, j) for i in range(board.size)) for j in range(board.size)))
    print(sum(sum(board.calc_score_yi(i, j) for i in range(board.size)) for j in range(board.size)))
    print(sum(sum(board.calc_score_yj(i, j) for i in range(board.size)) for j in range(board.size)))
    print(board.calc_score())
