from collections import defaultdict

class Day3:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")
    self.rows, self.cols = len(self.input), len(self.input[0])
    self.directions = [[0,1],[0,-1],[1,0],[-1,0],[-1,-1],[-1,1],[1,1],[1,-1]]

  def adjContainsSymbol(self, r, c):
    for dr, dc in self.directions:
      nr, nc = r + dr, c + dc
      if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.input[nr][nc].isnumeric() and self.input[nr][nc] != '.':
        return True
    return False

  def findAdjGears(self, r, c):
    gears = set()
    for dr, dc in self.directions:
      nr, nc = r + dr, c + dc
      if 0 <= nr < self.rows and 0 <= nc < self.cols and self.input[nr][nc] == '*':
        gears.add((nr, nc))
    return gears

  def p1(self):
    sumPartNumbers = 0
    for r in range(self.rows):
      c = 0
      while c < self.cols:
        if self.input[r][c].isnumeric():
          startNum = c
          partNumber = False
          while c < self.cols and self.input[r][c].isnumeric():
            if not partNumber and self.adjContainsSymbol(r, c): # avoid recomputation once found to be a partNumber
              partNumber = True
            c += 1
          endNumPlusOne = c
          if partNumber: sumPartNumbers += int(self.input[r][startNum:endNumPlusOne])
        c += 1
    print('p1', sumPartNumbers)

  def p2(self):
    gearsInSchematic = defaultdict(list)
    sumGearRatios = 0

    for r in range(self.rows):
      c = 0
      while c < self.cols:
        if self.input[r][c].isnumeric():
          startNum = c
          gearsAdjacent = set() # unique gears adjacent to this partNumber
          while c < self.cols and self.input[r][c].isnumeric():
            gearsAdjacent = gearsAdjacent | self.findAdjGears(r, c)
            c += 1
          endNumPlusOne = c
          partNumber = int(self.input[r][startNum:endNumPlusOne])
          for gear in gearsAdjacent: # populate gearsInSchematic lists with partNumbers adjacent to a potential gear as the key
            gearsInSchematic[gear].append(partNumber)
        c += 1

    # find gears, exactly 2 partNumbers adjacent, and sum the gear ratio
    for gear in gearsInSchematic:
      if len(gearsInSchematic[gear]) == 2:
        sumGearRatios += gearsInSchematic[gear][0] * gearsInSchematic[gear][1]
    print('p2', sumGearRatios)

d3 = Day3()
d3.p1()
d3.p2()