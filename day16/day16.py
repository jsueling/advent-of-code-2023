from collections import defaultdict, deque

class Day16:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")
    
    # credits to # https://stackoverflow.com/a/19189356 for recursive default dict
    def rec_dd():
      return defaultdict(rec_dd)

    self.outGoingDirections = rec_dd()

    self.outGoingDirections['|']['W'] = ['N', 'S'] # 2nd key is incoming direction of beam
    self.outGoingDirections['|']['E'] = ['N', 'S']

    self.outGoingDirections['-']['N'] = ['E', 'W']
    self.outGoingDirections['-']['S'] = ['E', 'W']

    self.outGoingDirections['/']['N'] = ['E']
    self.outGoingDirections['/']['E'] = ['N']
    self.outGoingDirections['/']['S'] = ['W']
    self.outGoingDirections['/']['W'] = ['S']

    self.outGoingDirections["\\"]['N'] = ['W']
    self.outGoingDirections["\\"]['E'] = ['S']
    self.outGoingDirections["\\"]['S'] = ['E']
    self.outGoingDirections["\\"]['W'] = ['N']

    self.directions = {
      'N': [-1, 0],
      'E': [0, 1],
      'S': [1, 0],
      'W': [0, -1]
    }

    self.ROWS, self.COLS = len(self.input), len(self.input[0])

  def countEnergisedTiles(self, firstTile):

    tiles = set()

    visit = set() # avoid endless loop by tracking (row, col, direction)

    q = deque([firstTile])

    while q:

      for _ in range(len(q)):

        r, c, direction = q.popleft()

        tiles.add((r, c))

        symbol = self.input[r][c]

        if symbol in self.outGoingDirections and direction in self.outGoingDirections[symbol]:
          for outDir in self.outGoingDirections[symbol][direction]:
            dr, dc = self.directions[outDir]
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.ROWS and 0 <= nc < self.COLS and (nr, nc, outDir) not in visit:
              visit.add((nr, nc, outDir))
              q.append((nr, nc, outDir))
        else:
          dr, dc = self.directions[direction]
          nr, nc = r + dr, c + dc
          if 0 <= nr < self.ROWS and 0 <= nc < self.COLS and (nr, nc, direction) not in visit:
            visit.add((nr, nc, direction))
            q.append((nr, nc, direction))
    
    return len(tiles)

  def p1(self):
    print("p1", self.countEnergisedTiles((0, 0, 'E')))

  def p2(self):

    maxEnergisedTiles = 0

    for row in range(self.ROWS):
      maxEnergisedTiles = max(
        maxEnergisedTiles,
        self.countEnergisedTiles((row, 0, 'E')),
        self.countEnergisedTiles((row, self.COLS-1, 'W'))
      )

    for col in range(self.COLS):
      maxEnergisedTiles = max(
        maxEnergisedTiles,
        self.countEnergisedTiles((0, col, 'S')),
        self.countEnergisedTiles((self.ROWS-1, col, 'N'))
      )

    print("p2", maxEnergisedTiles)

d16 = Day16()
d16.p1()
d16.p2()