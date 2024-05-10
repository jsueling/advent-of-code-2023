from collections import defaultdict

class Day23:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")

    self.ROWS, self.COLS = len(self.input), len(self.input[0])

    self.directions = [[-1,0], [1,0], [0,1], [0,-1]]

    self.start, self.end = (0, 1), (self.ROWS-1, self.COLS-2)
  
  def p1(self):

    # all paths are single corridors which gives us no choice unless there is a fork

    # each fork is a node, start is the first node, end is the last

    # Create adjacency list between nodes with steps as weights of the edges

    def isFork(r, c):
        slopes = 0
        if r + 1 < self.ROWS and self.input[r+1][c] == 'v':
          slopes += 1
        if r - 1 >= 0 and self.input[r-1][c] == '^':
          slopes += 1
        if c + 1 < self.COLS and self.input[r][c+1] == '>':
          slopes += 1
        if c - 1 >= 0 and self.input[r][c-1] == '<':
          slopes += 1
        return slopes > 1

    q = [(0, 1, self.start, 0, 1)]

    visit = set([self.start])

    neighbours = defaultdict(lambda: defaultdict(int))

    steps = 0

    # bfs populating the adjacency list with distances between nodes

    while q:
      nextLevel = []

      for r, c, src, lastSteps, lastDirection in q:

        dst = (r, c)

        if isFork(r, c) or dst == self.end:
          stepsFromPrevToThisFork = steps-lastSteps
          neighbours[src][dst] = max(neighbours[src][dst], stepsFromPrevToThisFork)

          # this node becomes the new src, and steps reset to count from this node
          lastSteps = steps
          src = (r, c)
        
        if 0 <= r + 1 < self.ROWS and self.input[r+1][c] in '.v' and lastDirection != 0:
          nextLevel.append((r + 1, c, src, lastSteps, 1))
        if 0 <= r - 1 < self.ROWS and self.input[r-1][c] in '.^' and lastDirection != 1:
          nextLevel.append((r - 1, c, src, lastSteps, 0))
        if 0 <= c + 1 < self.COLS and self.input[r][c+1] in '.>' and lastDirection != 3:
          nextLevel.append((r, c + 1, src, lastSteps, 2))
        if 0 <= c - 1 < self.COLS and self.input[r][c-1] in '.<' and lastDirection != 2:
          nextLevel.append((r, c - 1, src, lastSteps, 3))

      q = nextLevel

      steps += 1

    # for key in neighbours:
    #   print(key, neighbours[key])

    def getMaxSteps(src):

      if src == self.end:
        return 0

      cur = float("-inf")
      for dst in neighbours[src].keys():
        edge = neighbours[src][dst]
        cur = max(cur, edge + getMaxSteps(dst))
      return cur

    # explore every path with dfs traversing the adjacency list returning longest path

    print("p1", getMaxSteps(self.start))

  def p2(self):

    # nodes are now junctions as we can go up slopes, the graph is also now undirected

    def isJunction(r, c):
        slopes = 0
        if r + 1 < self.ROWS and self.input[r+1][c] in 'v^':
          slopes += 1
        if r - 1 >= 0 and self.input[r-1][c] in 'v^':
          slopes += 1
        if c + 1 < self.COLS and self.input[r][c+1] in '<>':
          slopes += 1
        if c - 1 >= 0 and self.input[r][c-1] in '<>':
          slopes += 1
        return slopes > 2

    neighbours = defaultdict(list)

    def dfs(r, c, visit, steps, prev):
      for dr, dc in self.directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < self.ROWS and 0 <= nc < self.COLS and self.input[nr][nc] != '#' and (nr, nc) not in visit:
          visit.add((nr, nc))
          if isJunction(nr, nc) or (nr, nc) == self.end:
            neighbours[prev].append([(nr, nc), steps + 1])
          elif (nr, nc) == self.start:
            neighbours[(0, 1)].append([prev, steps + 1])
          else:
            dfs(nr, nc, visit, steps + 1, prev)

    # populate neighbours using dfs
    # going from each node to every other node and recording the steps between

    for r in range(self.ROWS):
      for c in range(self.COLS):
        if isJunction(r, c):
          dfs(r, c, set([(r, c)]), 0, (r, c))

    # for key in neighbours:
    #   print(key, neighbours[key])

    junctionsVisited = set([(0, 1)])

    def getMaxSteps(src):

      if src == self.end:
        return 0

      cur = float("-inf")

      for dst, steps in neighbours[src]:
        if dst not in junctionsVisited:
          junctionsVisited.add(dst)
          cur = max(cur, steps + getMaxSteps(dst))
          junctionsVisited.remove(dst)

      return cur

    # explore every path using dfs from start returning the maximum steps
    # treating all slopes as normal paths and not stepping on the same tile twice

    print("p2", getMaxSteps(self.start))

d23 = Day23()
d23.p1()
d23.p2()