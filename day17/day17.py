from functools import cache
from heapq import heappop, heappush

class Day17:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")
  
    self.ROWS, self.COLS = len(self.input), len(self.input[0])

    self.directions = {
      'N': [-1, 0],
      'S': [1, 0],
      'E': [0, 1],
      'W': [0, -1]
    }

    self.turnMap = {
      'N': ['N', 'E', 'W'],
      'S': ['S', 'E', 'W'],
      'E': ['E', 'N', 'S'],
      'W': ['W', 'N', 'S']
    }

  def p1(self):

    def dijkstrasCrucibles():

      visit = set([(1, 0, 2, 'S'), (0, 1, 2, 'E')])

      heap = [(int(self.input[1][0]), 1, 0, 2, 'S'), (int(self.input[0][1]), 0, 1, 2, 'E')]

      while heap:
        cost, row, col, movesBeforeTurn, direction = heappop(heap)

        if (row, col) == (self.ROWS-1, self.COLS-1):
          return cost
        
        for nextDirection in self.turnMap[direction]:

          sameDirection = (nextDirection == direction)

          if sameDirection and movesBeforeTurn == 0:
            continue

          deltaRow, deltaCol = self.directions[nextDirection]

          nextRow, nextCol = row + deltaRow, col + deltaCol

          parameters = (nextRow, nextCol, (movesBeforeTurn - 1) if sameDirection else 2, nextDirection)

          if  0 <= nextRow < self.ROWS and 0 <= nextCol < self.COLS and parameters not in visit:
            visit.add(parameters)
            heappush(heap, (cost + int(self.input[nextRow][nextCol]), *parameters))

    print("p1", dijkstrasCrucibles())

  def p2(self):

    def dijkstrasUltraCrucibles():

      visit = set([(1, 0, 1, 'S'), (0, 1, 1, 'E')])

      heap = [(int(self.input[1][0]), 1, 0, 1, 'S'), (int(self.input[0][1]), 0, 1, 1, 'E')]

      while heap:
        cost, row, col, consecutiveMoves, direction = heappop(heap)

        if (row, col) == (self.ROWS-1, self.COLS-1):
          return cost
        
        for nextDirection in self.turnMap[direction]:

          sameDirection = (nextDirection == direction)

          if sameDirection and consecutiveMoves == 10:
            continue

          if consecutiveMoves < 4 and not sameDirection:
            continue

          deltaRow, deltaCol = self.directions[nextDirection]

          nextRow, nextCol = row + deltaRow, col + deltaCol

          parameters = (nextRow, nextCol, (consecutiveMoves + 1) if sameDirection else 1, nextDirection)

          if  0 <= nextRow < self.ROWS and 0 <= nextCol < self.COLS and parameters not in visit:
            visit.add(parameters)
            heappush(heap, (cost + int(self.input[nextRow][nextCol]), *parameters))

    print("p2", dijkstrasUltraCrucibles())

d17 = Day17()
d17.p1()
d17.p2()