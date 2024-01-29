class Day11:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")
    
    self.rows, self.cols = len(self.input), len(self.input)

    self.emptyRow = [True] * self.rows
    self.emptyCol = [True] * self.cols

    self.points = []

    for r in range(self.rows):
      for c in range(self.cols):
        if self.input[r][c] == '#':
          self.points.append((r,c))
          if self.emptyRow[r]:
            self.emptyRow[r] = False
          if self.emptyCol[c]:
            self.emptyCol[c] = False

  def p1(self):
    
    sumShortestLengths = 0

    n = len(self.points)
    for i in range(n-1):
      r1, c1 = self.points[i]
      for j in range(i + 1, n):
        r2, c2 = self.points[j]
        minR, minC, maxR, maxC = min(r1,r2), min(c1,c2), max(r1,r2), max(c1,c2)
        rowDiff = maxR - minR
        colDiff = maxC - minC

        for r in range(minR+1, maxR):
          if self.emptyRow[r]:
            rowDiff += 1

        for c in range(minC+1, maxC):
          if self.emptyCol[c]:
            colDiff += 1

        sumShortestLengths += rowDiff + colDiff

    print("p1", sumShortestLengths)

  def p2(self):
    sumShortestLengths = 0
    n = len(self.points)
    for i in range(n-1):
      r1, c1 = self.points[i]
      for j in range(i + 1, n):
        r2, c2 = self.points[j]
        minR, minC, maxR, maxC = min(r1,r2), min(c1,c2), max(r1,r2), max(c1,c2)
        rowDiff = maxR - minR
        colDiff = maxC - minC

        for r in range(minR+1, maxR):
          if self.emptyRow[r]: # "each empty row should be replaced with 1000000 empty rows", for each emptyRow add 999999
            rowDiff += 999999

        for c in range(minC+1, maxC):
          if self.emptyCol[c]:
            colDiff += 999999

        sumShortestLengths += rowDiff + colDiff

    print("p2", sumShortestLengths)

d11 = Day11()
d11.p1()
d11.p2()