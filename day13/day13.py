from collections import defaultdict

class Day13:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")

  def p1(self):

    resultSum = 0

    patterns = []
    pattern = []
    for i, line in enumerate(self.input):
      if line == '' or i == len(self.input)-1:
        patterns.append(pattern)
        pattern = []
      else:
        pattern.append(line)
    
    def reflectionBetween(prev, nxt, UPPER_BOUND, hashSymbolSet):
      while prev >= 0 and nxt < UPPER_BOUND:
        if hashSymbolSet[prev] != hashSymbolSet[nxt]:
          return False
        prev -= 1
        nxt += 1
      return True
    
    reflectionLines = {}

    for index, pattern in enumerate(patterns):

      colSet = defaultdict(set)
      rowSet = defaultdict(set) # rowSet[row] contains the indices of columns containing '#' at that row

      ROWS, COLS = len(pattern), len(pattern[0])

      for row in range(ROWS):
        for col in range(COLS):
          if pattern[row][col] == '#':
            rowSet[row].add(col)
            colSet[col].add(row)
    
      for i in range(0, ROWS-1, 1):
        prev, nxt = i, i + 1
        if reflectionBetween(prev, nxt, ROWS, rowSet):
          resultSum += 100 * (prev + 1)
          reflectionLines[index] = (prev, nxt, 'row')
      
      for i in range(0, COLS-1, 1):
        prev, nxt = i, i + 1
        if reflectionBetween(prev, nxt, COLS, colSet):
          resultSum += (prev + 1)
          reflectionLines[index] = (prev, nxt, 'col')
    
    # print(reflectionLines) # for debugging p2
    print("p1", resultSum)

  def p2(self):
    resultSum = 0

    patterns = []
    pattern = []
    for i, line in enumerate(self.input):
      if line == '' or i == len(self.input)-1:
        patterns.append(pattern)
        pattern = []
      else:
        pattern.append(line)
    
    def reflectionWithSmudgeBetween(prev, nxt, UPPER_BOUND, hashSymbolSet):

      smudgeFound = False

      while prev >= 0 and nxt < UPPER_BOUND:

        setDiff = hashSymbolSet[nxt] ^ hashSymbolSet[prev]

        if len(setDiff) > 1:
          return False
        
        if len(setDiff) == 1:
          if smudgeFound:
            return False
          smudgeFound = True

        prev -= 1
        nxt += 1

      return smudgeFound

    reflectionLinesWithSmudge = set([i for i in range(len(patterns))])

    for index, pattern in enumerate(patterns):

      colSet = defaultdict(set)
      rowSet = defaultdict(set)

      ROWS, COLS = len(pattern), len(pattern[0])

      for row in range(ROWS):
        for col in range(COLS):
          if pattern[row][col] == '#':
            rowSet[row].add(col)
            colSet[col].add(row)

      for i in range(0, ROWS-1):
        prev, nxt = i, i + 1
        if reflectionWithSmudgeBetween(prev, nxt, ROWS, rowSet):
          resultSum += 100 * (prev + 1)
          reflectionLinesWithSmudge.remove(index)
          
      for i in range(0, COLS-1):
        prev, nxt = i, i + 1
        if reflectionWithSmudgeBetween(prev, nxt, COLS, colSet):
          resultSum += (prev + 1)
          reflectionLinesWithSmudge.remove(index)

    # print(reflectionLinesWithSmudge) # for debugging, new reflection lines must be found and different from p1
    print("p2", resultSum)

d13 = Day13()
d13.p1()
d13.p2()