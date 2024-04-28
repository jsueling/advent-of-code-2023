from collections import defaultdict

class Day21:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")

  def p1(self):

    directions = [[-1,0],[1,0],[0,-1],[0,1]]

    ROWS, COLS = len(self.input), len(self.input[0])

    gardenPlotRows = { r: defaultdict(int) for r in range(ROWS)}

    for r in range(ROWS):
      for c in range(COLS):
        if self.input[r][c] == 'S':
          gardenPlotRows[r][c] += 1

    steps = 64

    for _ in range(steps):

      tmpGardenPlots = [[0] * COLS for _ in range(3)]

      for r in range(ROWS + 2):

        writeRow = r % 3

        if r < ROWS:

          for c in range(COLS):

            if self.input[r][c] == '#':
              continue

            for dr, dc in directions:
              nr, nc = r + dr, c + dc
              if 0 <= nr < ROWS and 0 <= nc < COLS and self.input[nr][nc] != '#' and nc in gardenPlotRows[nr]:
                tmpGardenPlots[writeRow][c] += gardenPlotRows[nr][nc]

        if r > 1:

          gardenPlotRows[r-2].clear()

          readRow = (r-2) % 3

          for c in range(COLS):
            if tmpGardenPlots[readRow][c] > 0:
              gardenPlotRows[r-2][c] = tmpGardenPlots[readRow][c]
              tmpGardenPlots[readRow][c] = 0

    # for r, columns in gardenPlotRows.items():
    #   print(r, columns)

    print("p1", sum([len(gardenRow) for gardenRow in gardenPlotRows.values()]))

  def p2(self):

    directions = [[-1,0],[1,0],[0,-1],[0,1]]

    ROWS, COLS = len(self.input), len(self.input[0])

    q = [(65, 65)]

    oddPlots = evenPlots = 0

    unseen = set()
    hashCount = 0

    for r in range(ROWS):
      for c in range(COLS):
        if self.input[r][c] == '#':
          hashCount += 1
        else:
          unseen.add((r,c))

    unseen.remove((65, 65))

    steps = 0
    while q:

      nextLevel = []
      if steps >= 130:
        print(q)
        # result [(0, 0), (0, 130), (130, 0), (130, 130)]
        # This shows that the furthest points from center S are the corners
        # +-65 each row and col which is exactly 130 from the center
        # all other plots are reachable in less steps

      for r, c in q:

        if (r + c) % 2 == 0:
          evenPlots += 1
        else:
          oddPlots += 1

        for dr, dc in directions:
          nr, nc = r + dr, c + dc
          if 0 <= nr < ROWS and 0 <= nc < COLS and self.input[nr][nc] != '#' and (nr, nc) in unseen:

            unseen.remove((nr, nc))
            nextLevel.append((nr, nc))

      steps += 1
      q = nextLevel

    stepsFromStart = 26501365

    fullMidToMidMapTraversals = stepsFromStart // COLS

    mapsFullyExploredInOneDirection = fullMidToMidMapTraversals - 1

    stepsRemaining = stepsFromStart % COLS

    print("steps remaining", stepsRemaining)

    oddMaps = (fullMidToMidMapTraversals - 1) ** 2

    evenMaps = fullMidToMidMapTraversals ** 2

    fullMapPlots = oddMaps * oddPlots + evenMaps * evenPlots

    def bfs(r, c, steps):
      
      reachablePlots = 0

      q = [(r, c)]
      seen = set()

      while steps > 0:
        nextLevel = []

        for r, c in q:
          
          for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and self.input[nr][nc] != '#' and (nr, nc) not in seen:

              seen.add((nr, nc))
              nextLevel.append((nr, nc))

        steps -= 1

        if steps % 2 == 0:
          reachablePlots += len(nextLevel)

        q = nextLevel

      return reachablePlots

    threeQuarterMaps = mapsFullyExploredInOneDirection

    oneQuarterMaps = threeQuarterMaps + 1

    poleMapPlots = (
      bfs(65, 0, 130) +
      bfs(65, 130, 130) +
      bfs(0, 65, 130) +
      bfs(130, 65, 130)
    )

    # print(bfs(65,65,64)) # should equal p1 result

    NEfrontierMapPlots = threeQuarterMaps * bfs(130, 0, 195) + oneQuarterMaps * bfs(130, 0, 64)

    NWfrontierMapPlots = threeQuarterMaps * bfs(130, 130, 195) + oneQuarterMaps * bfs(130, 130, 64)

    SEfrontierMapPlots = threeQuarterMaps * bfs(0, 0, 195) + oneQuarterMaps * bfs(0, 0, 64)

    SWfrontierMapPlots = threeQuarterMaps * bfs(0, 130, 195) + oneQuarterMaps * bfs(0, 130, 64)

    print(
      "p2",
      NEfrontierMapPlots +
      NWfrontierMapPlots +
      SEfrontierMapPlots +
      SWfrontierMapPlots +
      poleMapPlots +
      fullMapPlots
    )

# All that matters is the boundary of the furthest plots we can reach
# Using the repeating centre aisles we can travel 1 map mid-to-mid in any direction (Up Down Left Right) in the same distance
# We can use symmetry to count:
# the amount and types of partially explored maps
# the amount of fully explored maps
# and finally how many plots each yields to the result
# At the edges we will have some remainder steps.
# I backtracked the remainder steps to the correct point and used bfs to fill to find the correct plots able to be visited

d21 = Day21()
d21.p1()
d21.p2()