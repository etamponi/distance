import random
import sys

from time import time

from nearness import Board

def benchmark(size):
  board = Board(size)
  initial_score = board.score
  print("INITIAL SCORE:", initial_score)

  start = time()
  score = board.swap((0, 0), (0, 1))
  print("SWAP TIME:", time() - start)
  print("NEW SCORE:", score)

  start = time()
  peek_score = board.peek_swap((0, 0), (0, 1))
  print("PEEK SWAP TIME:", time() - start)
  print("PEEKED SCORE:", peek_score)
  assert(peek_score == initial_score)

  start = time()
  peek_score = board.peek_swap((0, 0), (0, 1))
  print("PEEK SWAP TIME:", time() - start)
  print("PEEKED SCORE:", peek_score)
  assert(peek_score == initial_score)

  start = time()
  board.skip()
  print("SKIPPING TIME:", time() - start)

  # Swap here, then peek the skipped state and verify it is skipped
  board.swap((0, 2), (0, 0))

  start = time()
  skip = board.peek_skipped((0, 2), (0, 0))
  print("SKIP CHECK TIME:", time() - start)
  assert(skip)

  start = time()
  random.shuffle(board.all_pairs)
  print("SHUFFLING ALL PAIRS:", time() - start)

  start = time()
  for pair in board.all_pairs[:min(len(board.all_pairs), 1000)]:
    board.peek_skipped(*pair)
    board.peek_swap(*pair)
    board.swap(*pair)
  print("PEEK UP AND SWAP UP TO 1000 TIMES TIME:", time() - start)

if __name__ == "__main__":
  size = int(sys.argv[1])
  benchmark(size)
