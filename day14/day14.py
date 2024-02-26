from collections import defaultdict
from bisect import bisect

class Cube:

  def __init__(self):
    self.incomingNorth = 0
    self.incomingEast = 0
    self.incomingSouth = 0
    self.incomingWest = 0
  
  def addNorth(self):
    self.incomingNorth += 1

  def addEast(self):
    self.incomingEast += 1

  def addSouth(self):
    self.incomingSouth += 1

  def addWest(self):
    self.incomingWest += 1

  def clearNorth(self):
    self.incomingNorth = 0

  def clearEast(self):
    self.incomingEast = 0

  def clearSouth(self):
    self.incomingSouth = 0

  def clearWest(self):
    self.incomingWest = 0
  
  def getStatus(self):
    return [self.incomingNorth, self.incomingEast, self.incomingSouth, self.incomingWest]

class Day14:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")
    with open("test.txt", "r") as f:
      self.test = f.read().split("\n")
  
  def p1(self):

    ROWS, COLS = len(self.input), len(self.input[0])

    totalLoadOnNorth = 0

    for col in range(COLS):

      roundedRocks = 0

      for row in range(ROWS-1,-2,-1):

        if row < 0 or (self.input[row][col] == '#' and roundedRocks > 0):

          i = row + 1

          for j in range(roundedRocks):
            totalLoadOnNorth += ROWS - (i + j)
          
          roundedRocks = 0

        elif self.input[row][col] == 'O':
          roundedRocks += 1

    print("p1", totalLoadOnNorth)

  def p2(self):

    ROWS, COLS = len(self.input), len(self.input[0])

    columnList = defaultdict(list) # columnList[col] stores row indices of cubes in this column
    rowList = defaultdict(list) # rowList[row] stores column indices of cubes in this row

    # cube objects that emulate cube shaped rocks, they are aware of how many rounded rocks
    # are leaning on them and from what direction.
    # They then transmit this info to the next cube objects in the spin cycle after each tilt

    # bisect to find index of next cube (add or subtract 1 depending on direction)
    # lookup the cube in list, add 1 to the incoming direction on this cube
    # which simulates a tilt where each rounded rock changes direction and hits another cube

    # and then instead of iterating over all cube objects, just have a record of those that now have rounded
    # rocks leaning on them from previous iteration

    cubes = [[None] * (COLS + 2) for _ in range(ROWS + 2)]

    # columnList and rowList are built in sorted order

    for row in range(ROWS):
      rowList[row].append(-1)
      cubes[row+1][0] = Cube()
      for col in range(COLS):
        if self.input[row][col] == '#':
          rowList[row].append(col)
          if not cubes[row+1][col+1]:
            cubes[row+1][col+1] = Cube()
      cubes[row+1][-1] = Cube()
      rowList[row].append(ROWS)

    for col in range(COLS):
      columnList[col].append(-1)
      cubes[0][col+1] = Cube()
      for row in range(ROWS):
        if self.input[row][col] == '#':
          columnList[col].append(row)
          if not cubes[row+1][col+1]:
            cubes[row+1][col+1] = Cube()
      cubes[-1][col+1] = Cube()
      columnList[col].append(COLS)

    # NWSE

    # do 1000000000 spin cycles
    for cycle in range(1, 1000000001):

      # N
      northCubes = set()

      if cycle == 1:
        for col in range(COLS):
          for row in range(ROWS):
            if self.input[row][col] == 'O':
              northIndexInColumnList = bisect(columnList[col], row) - 1
              nextNorthCubeRow = columnList[col][northIndexInColumnList]
              cubes[nextNorthCubeRow+1][col+1].addSouth()
              northCubes.add((nextNorthCubeRow, col))
      else:
        for row, col in eastCubes:
          for i in range(cubes[row+1][col+1].incomingWest):
            sphereCol = col - i - 1
            northIndexInColumnList = bisect(columnList[sphereCol], row) - 1
            nextNorthCubeRow = columnList[sphereCol][northIndexInColumnList]
            cubes[nextNorthCubeRow+1][sphereCol+1].addSouth()
            northCubes.add((nextNorthCubeRow, sphereCol))
          cubes[row+1][col+1].clearWest()

      # W
      westCubes = set()

      for row, col in northCubes:
        for i in range(cubes[row+1][col+1].incomingSouth):
          sphereRow = row + i + 1
          westIndexInRowList = bisect(rowList[sphereRow], col) - 1
          nextWestCubeCol = rowList[sphereRow][westIndexInRowList]
          cubes[sphereRow+1][nextWestCubeCol+1].addEast()
          westCubes.add((sphereRow, nextWestCubeCol))
        cubes[row+1][col+1].clearSouth()

      # S
      southCubes = set()

      for row, col in westCubes:
        for i in range(cubes[row+1][col+1].incomingEast):
          sphereCol = col + i + 1
          southIndexInColumnList = bisect(columnList[sphereCol], row)
          nextSouthCubeRow = columnList[sphereCol][southIndexInColumnList]
          cubes[nextSouthCubeRow+1][sphereCol+1].addNorth()
          southCubes.add((nextSouthCubeRow, sphereCol))
        cubes[row+1][col+1].clearEast()

      # E
      eastCubes = set()
      
      for row, col in southCubes:
        for i in range(cubes[row+1][col+1].incomingNorth):
          sphereRow = row - i - 1
          eastIndexInRowList = bisect(rowList[sphereRow], col)
          nextEastCubeCol = rowList[sphereRow][eastIndexInRowList]
          cubes[sphereRow+1][nextEastCubeCol+1].addWest()
          eastCubes.add((sphereRow, nextEastCubeCol))
        cubes[row+1][col+1].clearNorth()
      
      # count load on north support beams after 1 cycle
      northLoad = 0
      for r in range(ROWS+2):
        for c in range(COLS+2):
          if cubes[r][c]:
            actualRow = r-1
            northLoad += (ROWS - actualRow) * cubes[r][c].incomingWest

      print(cycle, northLoad) # extrapolated to find answer after finding repeating state

d14 = Day14()
d14.p1()
d14.p2()