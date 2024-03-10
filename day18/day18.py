from collections import defaultdict, Counter

class Day18:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")
    
    self.directionInstruction = {
      'U': [-1, 0],
      'D': [1, 0],
      'L': [0, -1],
      'R': [0, 1]
    }

  def p1(self):

    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    
    trench = set([(0,0)])

    row, col = 0, 0

    for line in self.input:

      direction, stepString, colour = line.split()

      steps = int(stepString)

      deltaRow, deltaCol = self.directionInstruction[direction]

      for step in range(steps):
        row += deltaRow
        col += deltaCol
        trench.add((row, col))

    q = [(-1, 0)] # guess which spot is inside the loop either (-1, 0) or (1, -1) based on input

    # flood fill using BFS
    while q:
      nextLevel = []
      for r, c in q:
        for dr, dc in directions:
          nr, nc = r + dr, c + dc
          nextSpot = (nr, nc)
          if nextSpot not in trench:
            trench.add(nextSpot)
            nextLevel.append(nextSpot)
      q = nextLevel

    print("p1", len(trench))

  def p2(self):
      
    # finding areas this big using pixel flood fill is computationally inefficient
    # credits to this algorithm: https://stackoverflow.com/a/47254061

    # some assertions we have to make:
    # 1. trench lines don't cross
    # 2. direction instructions follow pattern L/R then U/D i.e. no L L U U or L R D U

    # How do we know which area is inside?:
    # 1. trial answers considering each of 2 directions
    # 2. Any blocks on boundary without boundary edge must consider all other touching edges pointing away from this block or answer is invalid

    # credits to # https://stackoverflow.com/a/19189356 for recursive default dict
    def rec_dd():
      return defaultdict(rec_dd)

    nextInsideMap = rec_dd()

    nextInsideMap['U']['L']['L'] = 'D'
    nextInsideMap['U']['L']['R'] = 'U'

    nextInsideMap['U']['R']['L'] = 'U'
    nextInsideMap['U']['R']['R'] = 'D'

    nextInsideMap['D']['L']['L'] = 'U'
    nextInsideMap['D']['L']['R'] = 'D'

    nextInsideMap['D']['R']['L'] = 'D'
    nextInsideMap['D']['R']['R'] = 'U'

    nextInsideMap['L']['U']['U'] = 'R'
    nextInsideMap['L']['U']['D'] = 'L'

    nextInsideMap['L']['D']['U'] = 'L'
    nextInsideMap['L']['D']['D'] = 'R'

    nextInsideMap['R']['U']['U'] = 'L'
    nextInsideMap['R']['U']['D'] = 'R'

    nextInsideMap['R']['D']['U'] = 'R'
    nextInsideMap['R']['D']['D'] = 'L'

    indexToDirection = [[0, 1], [1, 0], [0, -1], [-1, 0]]

    indexToString = ['R', 'D', 'L', 'U']

    row, col = 0, 0

    verticalTrenchEdges = rec_dd()
    horizontalTrenchEdges = rec_dd()

    uniqueRows = set()
    uniqueCols = set()

    for index, line in enumerate(self.input):

      _, _, colour = line.split()

      instruction = colour[1:-1]

      hexSteps = instruction[1:-1]
      directionIndex = int(instruction[-1])

      steps = int(hexSteps, 16)
      
      curDir = indexToString[directionIndex]

      startRow = row
      startCol = col

      # print(curDir, steps)

      deltaRow, deltaCol = indexToDirection[directionIndex]

      if index == 0: # Right is first step in both example and input
        col += deltaCol * steps
        firstDirectionInside = 'D' # could be either 'U' or 'D'
        horizontalTrenchEdges[0][(0, col)] = firstDirectionInside
        uniqueCols.add(0)
        uniqueCols.add(col)
        uniqueRows.add(0)
        prevDir = 'R'
        lastInsideDirection = firstDirectionInside
        continue

      nextInsideDirection = nextInsideMap[prevDir][curDir][lastInsideDirection]

      if directionIndex == 0 or directionIndex == 2: # horizontal direction index
        col += deltaCol * steps
        horizontalTrenchEdges[row][(min(startCol, col), max(startCol, col))] = nextInsideDirection
        uniqueCols.add(col)
      else:
        row += deltaRow * steps
        verticalTrenchEdges[col][(min(startRow, row), max(startRow, row))] = nextInsideDirection
        uniqueRows.add(row)

      prevDir = curDir
      lastInsideDirection = nextInsideDirection
    
    sortedRows = sorted(uniqueRows)
    sortedCols = sorted(uniqueCols)

    def isCoincidentLine(A, B): # where line A length is less than or equal line B length
      s1, e1 = A
      s2, e2 = B
      return s1 >= s2 and e1 <= e2

    def rectangleIsInsideTrench(r1, r2, c1, c2):
      
      # check if any border of this rectangle is coincident with a known trench edge
      # and the direction of inside the trench for that edge verifies the rectangle as inside the trench

      topEdges = horizontalTrenchEdges[r1]
      for col1, col2 in topEdges.keys():
        if isCoincidentLine((c1, c2), (col1, col2)):
          return topEdges[(col1, col2)] == 'D'
      
      botEdges = horizontalTrenchEdges[r2]
      for col1, col2 in botEdges.keys():
        if isCoincidentLine((c1, c2), (col1, col2)):
          return botEdges[(col1, col2)] == 'U'

      leftEdges = verticalTrenchEdges[c1]
      for row1, row2 in leftEdges.keys():
        if isCoincidentLine((r1, r2), (row1, row2)):
          return leftEdges[(row1, row2)] == 'R'

      rightEdges = verticalTrenchEdges[c2]
      for row1, row2 in rightEdges.keys():
        if isCoincidentLine((r1, r2), (row1, row2)):
          return rightEdges[(row1, row2)] == 'L'
      
      return False # returning false means we can't know for certain

    adjList = defaultdict(list) # maps rectangle edges to the 2 rectangles it borders
    for i in range(len(sortedRows)-1):
      r1, r2 = sortedRows[i], sortedRows[i+1]
      for j in range(len(sortedCols)-1):
        c1, c2 = sortedCols[j], sortedCols[j+1]
        adjList[('V', c1, r1, r2)].append((r1, r2, c1, c2))
        adjList[('V', c2, r1, r2)].append((r1, r2, c1, c2))
        adjList[('H', r1, c1, c2)].append((r1, r2, c1, c2))
        adjList[('H', r2, c1, c2)].append((r1, r2, c1, c2))

    self.areaDoubleCountedEdges = 0

    def floodFill(firstRectangle, rectanglesVisited, rectEdges):

      q = [firstRectangle]

      while q:

        nextLevel = []
        for r1, r2, c1, c2 in q:
          
          topEdgeDoesNotCoincideWithTrenchEdge = not any([isCoincidentLine((c1, c2), (col1, col2)) for col1, col2 in horizontalTrenchEdges[r1].keys()])
          botEdgeDoesNotCoincideWithTrenchEdge = not any([isCoincidentLine((c1, c2), (col1, col2)) for col1, col2 in horizontalTrenchEdges[r2].keys()])
          leftEdgeDoesNotCoincideWithTrenchEdge = not any([isCoincidentLine((r1, r2), (row1, row2)) for row1, row2 in verticalTrenchEdges[c1].keys()])
          rightEdgeDoesNotCoincideWithTrenchEdge = not any([isCoincidentLine((r1, r2), (row1, row2)) for row1, row2 in verticalTrenchEdges[c2].keys()])

          if any([
            r1 == sortedRows[0] and topEdgeDoesNotCoincideWithTrenchEdge,
            r2 == sortedRows[-1] and botEdgeDoesNotCoincideWithTrenchEdge,
            c1 == sortedRows[0] and leftEdgeDoesNotCoincideWithTrenchEdge,
            c2 == sortedCols[-1] and rightEdgeDoesNotCoincideWithTrenchEdge
          ]):
            print('reached boundary outside of trench') # if floodFill visits a rectangle on the boundary where there is no trench edge

          # We can explore (top, bot, left, right) rectangles through a rectangle's edge if it doesn't coincide with a trench edge

          if topEdgeDoesNotCoincideWithTrenchEdge:

            topEdge = ('H', r1, c1, c2)

            if topEdge not in rectEdges:
              # make sure each rectangle edge is only counted once
              rectangleEdges.add(topEdge)
              self.areaDoubleCountedEdges += c2 - c1 + 1
            
            for adjacentRectangle in adjList[topEdge]:
              if adjacentRectangle not in rectanglesVisited:
                nextLevel.append(adjacentRectangle)
                rectanglesVisited.add(adjacentRectangle)

          if botEdgeDoesNotCoincideWithTrenchEdge:

            botEdge = ('H', r2, c1, c2)

            if botEdge not in rectEdges:
              rectEdges.add(botEdge)
              self.areaDoubleCountedEdges += c2 - c1 + 1
            
            for adjacentRectangle in adjList[('H', r2, c1, c2)]:
              if adjacentRectangle not in rectanglesVisited:
                nextLevel.append(adjacentRectangle)
                rectanglesVisited.add(adjacentRectangle)
          
          if leftEdgeDoesNotCoincideWithTrenchEdge:

            leftEdge = ('V', c1, r1, r2)

            if leftEdge not in rectEdges:
              rectEdges.add(leftEdge)
              self.areaDoubleCountedEdges += r2 - r1 + 1
            
            for adjacentRectangle in adjList[('V', c1, r1, r2)]:
              if adjacentRectangle not in rectanglesVisited:
                nextLevel.append(adjacentRectangle)
                rectanglesVisited.add(adjacentRectangle)
          
          if rightEdgeDoesNotCoincideWithTrenchEdge:

            rightEdge = ('V', c2, r1, r2)

            if rightEdge not in rectEdges:
              rectEdges.add(rightEdge)
              self.areaDoubleCountedEdges += r2 - r1 + 1
            
            for adjacentRectangle in adjList[('V', c2, r1, r2)]:
              if adjacentRectangle not in rectanglesVisited:
                nextLevel.append(adjacentRectangle)
                rectanglesVisited.add(adjacentRectangle)

        q = nextLevel

    rectanglesInTrench = set()
    rectangleEdges = set()

    for i in range(len(sortedRows)-1):
      r1, r2 = sortedRows[i], sortedRows[i+1]
      for j in range(len(sortedCols)-1):
        c1, c2 = sortedCols[j], sortedCols[j+1]
        if rectangleIsInsideTrench(r1, r2, c1, c2): # rectangle inside trench makes it a candidate for floodFill
          rectanglesInTrench.add((r1, r2, c1, c2))
          floodFill((r1, r2, c1, c2), rectanglesInTrench, rectangleEdges)

    cornerCount = Counter() # see doubleCounting

    for r1, r2, c1, c2 in rectanglesInTrench:
      cornerCount[(r1, c1)] += 1
      cornerCount[(r2, c1)] += 1
      cornerCount[(r1, c2)] += 1
      cornerCount[(r2, c2)] += 1
    
    fourWayCorners = sum([1 if freq == 4 else 0 for freq in cornerCount.values()])

    print("p2", sum([((r2-r1+1) * (c2-c1+1)) for r1, r2, c1, c2 in rectanglesInTrench]) - self.areaDoubleCountedEdges + fourWayCorners)

    # optimisations:
    # 1. Either (r1 == 0 and c1 == 0) or (c1 == 0 and r2 == 0) is always the first rectangle inside the trench as
    # both input and example have right as first direction
    # no need to record which direction is inside the trench for every rectangle
    # and then find first rectangle considered inside the trench to start the floodFill

d18 = Day18()
d18.p1()
d18.p2()