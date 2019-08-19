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

class Cell:
    # Original x, y coordinates
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __repr__(self):
        return "({:02d},{:02d})".format(self.x, self.y)

class Board:
    def __init__(self, size):
        self.size = size
        self.cells = [ [ Cell(i, j) for j in range(size) ] for i in range(size) ]
        self.dist = [ [self.calc_dist(i0, i) for i in range(size) ] for i0 in range(size) ]
        self.sum_dist_xi = [ [self.calc_sum_dist_xi(x_i0_j0, i) for i in range(size)] for x_i0_j0 in range(size) ]
        self.sum_dist_yi = [ [self.calc_sum_dist_yi(y_i0_j0, i) for i in range(size)] for y_i0_j0 in range(size) ]
        self.sum_dist_xj = [ [self.calc_sum_dist_xj(x_i0_j0, j) for j in range(size)] for x_i0_j0 in range(size) ]
        self.sum_dist_yj = [ [self.calc_sum_dist_yj(y_i0_j0, j) for j in range(size)] for y_i0_j0 in range(size) ]

        self.score_xi = sum(sum(self.calc_score_xi(i, j) for i in range(size)) for j in range(size))
        self.score_yi = sum(sum(self.calc_score_yi(i, j) for i in range(size)) for j in range(size))
        self.score_xj = sum(sum(self.calc_score_xj(i, j) for i in range(size)) for j in range(size))
        self.score_yj = sum(sum(self.calc_score_yj(i, j) for i in range(size)) for j in range(size))

        self.score = self.calc_score()
    
    def __repr__(self):
        return "\n".join(str(line) for line in self.cells)

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

    def calc_score_xi(self, i0, j0):
        x_i0_j0 = self.cells[i0][j0].x
        return sum(self.dist[i0][i] * self.sum_dist_xi[x_i0_j0][i] for i in range(self.size))

    def calc_score_yi(self, i0, j0):
        y_i0_j0 = self.cells[i0][j0].y
        return sum(self.dist[i0][i] * self.sum_dist_yi[y_i0_j0][i] for i in range(self.size))

    def calc_score_xj(self, i0, j0):
        x_i0_j0 = self.cells[i0][j0].x
        return sum(self.dist[j0][j] * self.sum_dist_xj[x_i0_j0][j] for j in range(self.size))

    def calc_score_yj(self, i0, j0):
        y_i0_j0 = self.cells[i0][j0].y
        return sum(self.dist[j0][j] * self.sum_dist_yj[y_i0_j0][j] for j in range(self.size))

    def calc_score(self):
        return (self.score_xi + self.score_xj + self.score_yi + self.score_yj) / 2 - BOUNDS[self.size]

    def swap(self, i0, j0, i1, j1):
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
            for x in range(self.size):
                self.sum_dist_xi[x][i0] += self.dist[x][x1] - self.dist[x][x0]
                self.sum_dist_xi[x][i1] += self.dist[x][x0] - self.dist[x][x1]

                self.sum_dist_xj[x][j0] += self.dist[x][x1] - self.dist[x][x0]
                self.sum_dist_xj[x][j1] += self.dist[x][x0] - self.dist[x][x1]

        y0, y1 = self.cells[i0][j0].y, self.cells[i1][j1].y
        if y0 != y1:
            for y in range(self.size):
                self.sum_dist_yi[y][i0] += self.dist[y][y1] - self.dist[y][y0]
                self.sum_dist_yi[y][i1] += self.dist[y][y0] - self.dist[y][y1]

                self.sum_dist_yj[y][j0] += self.dist[y][y1] - self.dist[y][y0]
                self.sum_dist_yj[y][j1] += self.dist[y][y0] - self.dist[y][y1]

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

def matrix(m):
    return "\n".join(" ".join("{: 3d}".format(d) for d in line) for line in m)

import nearness

if __name__ == "__main__":
    board = Board(4)
    b = nearness.Board(4)

    # print(board.score, b.score)
    # print("")

    # print(matrix(board.sum_dist_yi))
    # print("")

    print(board.score_xi, board.score_xj, board.score_yi, board.score_yj, board.score)
    print(sum(sum(board.calc_score_xi(i, j) for i in range(board.size)) for j in range(board.size)))
    print(sum(sum(board.calc_score_xj(i, j) for i in range(board.size)) for j in range(board.size)))
    print(sum(sum(board.calc_score_yi(i, j) for i in range(board.size)) for j in range(board.size)))
    print(sum(sum(board.calc_score_yj(i, j) for i in range(board.size)) for j in range(board.size)))
    print(board.calc_score(), b.score)

    board.swap(0, 1, 2, 3)
    board.swap(3, 2, 1, 0)
    board.swap(2, 1, 3, 0)
    # board.swap(2, 1, 3, 0)
    # board.swap(3, 2, 0, 1)
    # board.swap(0, 1, 2, 3)
    b.swap((0, 1), (2, 3))
    b.swap((3, 2), (1, 0))
    b.swap((2, 1), (3, 0))
    # b.swap((2, 1), (3, 0))
    # b.swap((3, 2), (1, 0))
    # b.swap((0, 1), (2, 3))

    # print(matrix([ [board.calc_sum_dist_yi(a, b) for b in range(board.size)] for a in range(board.size) ]))
    # print("")

    # print(matrix(board.sum_dist_yi))
    # print("")

    print(board.score_xi, board.score_xj, board.score_yi, board.score_yj, board.score)
    print(sum(sum(board.calc_score_xi(i, j) for i in range(board.size)) for j in range(board.size)))
    print(sum(sum(board.calc_score_xj(i, j) for i in range(board.size)) for j in range(board.size)))
    print(sum(sum(board.calc_score_yi(i, j) for i in range(board.size)) for j in range(board.size)))
    print(sum(sum(board.calc_score_yj(i, j) for i in range(board.size)) for j in range(board.size)))
    print(board.calc_score(), b.score)
