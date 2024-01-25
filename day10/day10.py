from collections import defaultdict

class Day10:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")

    self.rows, self.cols = len(self.input), len(self.input[0])

    # | is a vertical pipe connecting north and south.
    # - is a horizontal pipe connecting east and west.
    # L is a 90-degree bend connecting north and east.
    # J is a 90-degree bend connecting north and west.
    # 7 is a 90-degree bend connecting south and west.
    # F is a 90-degree bend connecting south and east.

    self.directions = [[1,0],[-1,0],[0,1],[0,-1]]

    self.outgoingDir = [{} for _ in range(4)]

    # outgoingDir receives an incoming direction and returns an outgoing direction
    # given that the pipe is a single continuous loop

    DOWN = 0
    UP = 1
    RIGHT = 2
    LEFT = 3

    self.outgoingDir[DOWN]['|'] = DOWN
    self.outgoingDir[DOWN]['L'] = RIGHT
    self.outgoingDir[DOWN]['J'] = LEFT

    self.outgoingDir[UP]['|'] = UP
    self.outgoingDir[UP]['7'] = LEFT
    self.outgoingDir[UP]['F'] = RIGHT

    self.outgoingDir[RIGHT]['-'] = RIGHT
    self.outgoingDir[RIGHT]['J'] = UP
    self.outgoingDir[RIGHT]['7'] = DOWN

    self.outgoingDir[LEFT]['-'] = LEFT
    self.outgoingDir[LEFT]['L'] = UP
    self.outgoingDir[LEFT]['F'] = DOWN

    self.pipe = set()

  def p1(self):

    def pipeBFS(r, c):

      q = []
      for dirIndex, (dr, dc) in enumerate(self.directions):
        nr, nc = r + dr, c + dc
        if 0 <= nr < self.rows and 0 <= nc < self.cols and self.input[nr][nc] in self.outgoingDir[dirIndex]:
          q.append((nr, nc, dirIndex))

      steps = 1
      while q:
        cur = []
        for node in q:
          r, c, incomingDir = node
          if (r, c) in self.pipe:
            # for r in range(self.rows):
            #   print(r, "".join([(self.input[r][c] if (r,c) not in self.pipe else "*") for c in range(len(self.input[r]))]))
            return steps
          self.pipe.add((r,c))
          pipe = self.input[r][c]
          outgoingDir = self.outgoingDir[incomingDir][pipe]
          dr, dc = self.directions[outgoingDir]
          nr, nc = r + dr, c + dc
          cur.append((nr, nc, outgoingDir))
        q = cur
        steps += 1

    for r, line in enumerate(self.input):
      for c, char in enumerate(line):
        if char == 'S':
          print("p1", pipeBFS(r,c))
          return

  def p2(self):

    def directionToSearch(pipe, direction):
      match pipe:
        case '|':
          match direction:
            case 'L':
              return [
                [-1,-1],
                [0,-1],
                [1,-1]
              ]
            case 'R':
              return [
                [-1,1],
                [0,1],
                [1,1]
              ]
        case '7':
          match direction:
            case 'T':
              return [
                [-1,-1],
                [-1,0],
                [-1,1],
                [0,1],
                [1,1]
              ]
            case 'B':
              return [
                [1,-1]
              ]
        case 'F':
          match direction:
            case 'T':
              return [
                [1,-1],
                [0,-1],
                [-1,-1],
                [-1,0],
                [-1,1]
              ]
            case 'B':
              return [
                [1,1]
              ]
        case 'J':
          match direction:
            case 'T':
              return [
                [-1,-1]
              ]
            case 'B':
              return [
                [1,-1],
                [1,0],
                [1,1],
                [0,1],
                [-1,1]
              ]
        case 'L':
          match direction:
            case 'T':
              return [
                [-1,1]
              ]
            case 'B':
              return [
                [-1,-1],
                [0,-1],
                [1,-1],
                [1,0],
                [1,1]
              ]
        case '-':
          match direction:
            case 'T':
              return [
                [-1,-1],
                [-1,0],
                [-1,1]
              ]
            case 'B':
              return [
                [1,-1],
                [1,0],
                [1,1]
              ]
      print("unreachable")
  
    # credits to # https://stackoverflow.com/a/19189356 for recursive default dict
    def rec_dd():
      return defaultdict(rec_dd)

    pipeMap = rec_dd()

    DOWN = 0
    UP = 1
    RIGHT = 2
    LEFT = 3

    # PREV (last pipe), CUR (this pipe), DIRECTION (from prev to cur), INSIDE (which direction PREV considered inside the loop)
    # accessing pipeMap with these parameters returns which direction is now considered inside the loop by CUR
    
    pipeMap['|']['L'][DOWN]['R'] = 'T' # going from | to an L going down where right was considered inside the loop by |, L considers the inside of the loop to be top
    pipeMap['|']['L'][DOWN]['L'] = 'B'
    pipeMap['|']['J'][DOWN]['R'] = 'B'
    pipeMap['|']['J'][DOWN]['L'] = 'T'
    pipeMap['|']['|'][DOWN]['L'] = 'L'
    pipeMap['|']['|'][DOWN]['R'] = 'R'

    pipeMap['|']['7'][UP]['R'] = 'T'
    pipeMap['|']['7'][UP]['L'] = 'B'
    pipeMap['|']['F'][UP]['R'] = 'B'
    pipeMap['|']['F'][UP]['L'] = 'T'
    pipeMap['|']['|'][UP]['L'] = 'L'
    pipeMap['|']['|'][UP]['R'] = 'R'

    pipeMap['7']['|'][DOWN]['T'] = 'R'
    pipeMap['7']['|'][DOWN]['B'] = 'L'
    pipeMap['7']['L'][DOWN]['T'] = 'T'
    pipeMap['7']['L'][DOWN]['B'] = 'B'
    pipeMap['7']['J'][DOWN]['T'] = 'B'
    pipeMap['7']['J'][DOWN]['B'] = 'T'

    pipeMap['7']['-'][LEFT]['T'] = 'T'
    pipeMap['7']['-'][LEFT]['B'] = 'B'
    pipeMap['7']['L'][LEFT]['T'] = 'T'
    pipeMap['7']['L'][LEFT]['B'] = 'B'
    pipeMap['7']['F'][LEFT]['T'] = 'T'
    pipeMap['7']['F'][LEFT]['B'] = 'B'

    pipeMap['F']['|'][DOWN]['T'] = 'L'
    pipeMap['F']['|'][DOWN]['B'] = 'R'
    pipeMap['F']['L'][DOWN]['T'] = 'B'
    pipeMap['F']['L'][DOWN]['B'] = 'T'
    pipeMap['F']['J'][DOWN]['T'] = 'T'
    pipeMap['F']['J'][DOWN]['B'] = 'B'

    pipeMap['F']['-'][RIGHT]['T'] = 'T'
    pipeMap['F']['-'][RIGHT]['B'] = 'B'
    pipeMap['F']['7'][RIGHT]['T'] = 'T'
    pipeMap['F']['7'][RIGHT]['B'] = 'B'
    pipeMap['F']['J'][RIGHT]['T'] = 'T'
    pipeMap['F']['J'][RIGHT]['B'] = 'B'

    pipeMap['J']['|'][UP]['T'] = 'L'
    pipeMap['J']['|'][UP]['B'] = 'R'
    pipeMap['J']['7'][UP]['T'] = 'B'
    pipeMap['J']['7'][UP]['B'] = 'T'
    pipeMap['J']['F'][UP]['T'] = 'T'
    pipeMap['J']['F'][UP]['B'] = 'B'

    pipeMap['J']['-'][LEFT]['T'] = 'T'
    pipeMap['J']['-'][LEFT]['B'] = 'B'
    pipeMap['J']['L'][LEFT]['T'] = 'T'
    pipeMap['J']['L'][LEFT]['B'] = 'B'
    pipeMap['J']['F'][LEFT]['T'] = 'T'
    pipeMap['J']['F'][LEFT]['B'] = 'B'

    pipeMap['L']['|'][UP]['T'] = 'R'
    pipeMap['L']['|'][UP]['B'] = 'L'
    pipeMap['L']['7'][UP]['T'] = 'T'
    pipeMap['L']['7'][UP]['B'] = 'B'
    pipeMap['L']['F'][UP]['T'] = 'B'
    pipeMap['L']['F'][UP]['B'] = 'T'

    pipeMap['L']['-'][RIGHT]['T'] = 'T'
    pipeMap['L']['-'][RIGHT]['B'] = 'B'
    pipeMap['L']['7'][RIGHT]['T'] = 'T'
    pipeMap['L']['7'][RIGHT]['B'] = 'B'
    pipeMap['L']['J'][RIGHT]['T'] = 'T'
    pipeMap['L']['J'][RIGHT]['B'] = 'B'

    pipeMap['-']['-'][RIGHT]['T'] = 'T'
    pipeMap['-']['-'][RIGHT]['B'] = 'B'
    pipeMap['-']['J'][RIGHT]['T'] = 'T'
    pipeMap['-']['J'][RIGHT]['B'] = 'B'
    pipeMap['-']['7'][RIGHT]['T'] = 'T'
    pipeMap['-']['7'][RIGHT]['B'] = 'B'

    pipeMap['-']['-'][LEFT]['T'] = 'T'
    pipeMap['-']['-'][LEFT]['B'] = 'B'
    pipeMap['-']['L'][LEFT]['T'] = 'T'
    pipeMap['-']['L'][LEFT]['B'] = 'B'
    pipeMap['-']['F'][LEFT]['T'] = 'T'
    pipeMap['-']['F'][LEFT]['B'] = 'B'

    def countInside(r, c, insideSpaces):
      if (r,c) in self.pipe or (r,c) in insideSpaces:
        return

      insideSpaces.add((r,c))

      q = [(r, c)]

      while q:
        cur = []
        for r, c in q:
          for dr, dc in self.directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) not in self.pipe and (nr, nc) not in insideSpaces:
              insideSpaces.add((nr, nc))
              cur.append((nr, nc))
        q = cur

    def pipeBFS(r, c, inside):

      q = []
      for dirIndex, (dr, dc) in enumerate(self.directions):
        nr, nc = r + dr, c + dc
        if 0 <= nr < self.rows and 0 <= nc < self.cols and self.input[nr][nc] in self.outgoingDir[dirIndex]:
          q.append((nr, nc, dirIndex, '-', inside))

      insideSpaces = set()
      visitedPipes = set()
      while q:
        cur = []
        for node in q:
          r, c, incomingDir, lastPipe, lastInside = node

          if (r, c) in visitedPipes:
            # depending on which direction is initially considered inside the loop, one of the two calls will have a corner spot in
            return 0 if (self.rows-1, self.cols-1) in insideSpaces else len(insideSpaces)

          visitedPipes.add((r,c))

          pipe = self.input[r][c]
          outgoingDir = self.outgoingDir[incomingDir][pipe]
          dr, dc = self.directions[outgoingDir]
          nr, nc = r + dr, c + dc
          nextInside = pipeMap[lastPipe][pipe][incomingDir][lastInside]

          cur.append((nr, nc, outgoingDir, pipe, nextInside))

          for sr, sc in directionToSearch(pipe, nextInside):
            countInside(r + sr, c + sc, insideSpaces)

        q = cur

    for r, line in enumerate(self.input):
      for c, char in enumerate(line):
        if char == 'S':
          self.pipe.add((r, c))
          T = pipeBFS(r, c, 'T')
          B = pipeBFS(r, c, 'B')
          print("p2", T if T else B)
          return

d10 = Day10()
d10.p1()
d10.p2()