from collections import defaultdict

from heapq import heapify, heappop, heappush

class Day22:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")
  
    self.onTopOf = defaultdict(list)

    self.restingUnder = defaultdict(list)
    
    self.bricks = []

  def p1(self):
    
    # When all bricks are settled, graph an adjacency list where an edge represents
    # which bricks are resting on this brick

    # We can disintegrate a brick if:
    # no bricks are resting on this brick
    # all the bricks that are resting on this brick are resting on at least 1 other brick

    # Heap that we can pull the brick that is next closest to the floor
    # Dictionary representing the z-axis or layer of each rested brick

    # For each brick go layer by layer looking for intersections between itself and rested bricks
    # If found an interstection between rested brick:
    # find all in current layer
    # add edge to graph
    # update dictionary with new brick resting at layer + 1

    layer = defaultdict(list) # layer will only store the top face of each brick

    nextClosest = []

    for index, line in enumerate(self.input):

      brick = []
      start, end = line.split("~")

      for c1, c2 in zip(start.split(","), end.split(",")):
        c1, c2 = int(c1), int(c2)
        brick.extend([min(c1, c2), max(c1, c2)])

      # brick is now [Xmin, Xmax, Ymin, Ymax, Zmin, Zmax]

      nextClosest.append([brick[4], index])

      self.bricks.append(brick)

    heapify(nextClosest)

    # for brick in self.bricks:
    #   print(brick)

    while nextClosest:

      depth, index = heappop(nextClosest)

      bx1, bx2, by1, by2, bz1, bz2 = self.bricks[index]

      while depth > 0:

        intersections = []

        foundIntersection = False

        if depth in layer:

          for restedBrick in layer[depth]:

            rx1, rx2, ry1, ry2, restedIndex = restedBrick

            if (bx2 < rx1 or bx1 > rx2) or (by1 > ry2 or by2 < ry1):
              continue
            
            self.restingUnder[index].append(restedIndex)

            self.onTopOf[restedIndex].append(index)

            foundIntersection = True

        if foundIntersection: # collision found so this brick comes to rest

          newBrick = [bx1, bx2, by1, by2, index]

          depthAtTopOfBrick = depth + 1

          if bz1 != bz2: # this brick is vertical if true
            depthAtTopOfBrick += bz2-bz1

          layer[depthAtTopOfBrick].append(newBrick)

          break

        depth -= 1

      if depth == 0: # on the floor

        newBrick = [bx1, bx2, by1, by2, index]

        depthAtTopOfNextBrick = depth + 1

        if bz1 != bz2: # this brick is vertical if true
          depthAtTopOfNextBrick += bz2-bz1

        layer[depthAtTopOfNextBrick].append(newBrick)

    disintegrationTargets = 0

    for i in range(len(self.bricks)):

      if i not in self.onTopOf: # brick i has no bricks rested on top of it
        disintegrationTargets += 1
      else:
        if all([len(self.restingUnder[j]) > 1 for j in self.onTopOf[i]]):
          # all bricks resting on top of this brick have more than one brick under them making this brick safe to disintegrate
          disintegrationTargets += 1

    print("p1", disintegrationTargets)

  def p2(self):

    def dfs(i, disintegrated):

      for brickOnTop in self.onTopOf[i]:
        
        if all([brickUnder in disintegrated for brickUnder in self.restingUnder[brickOnTop]]):

          if brickOnTop not in disintegrated:

            disintegrated.add(brickOnTop)

            dfs(brickOnTop, disintegrated)
      
      return len(disintegrated)

    sumOtherBricksFalling = 0

    for i in range(len(self.bricks)):
      sumOtherBricksFalling += dfs(i, set([i])) - 1
    
    print("p2", sumOtherBricksFalling)

d22 = Day22()
d22.p1()
d22.p2()