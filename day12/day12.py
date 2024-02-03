import re
import functools

class Day12:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")

    with open("input2.txt", "w") as f:
      new_lines = []
      for i, line in enumerate(self.input):
        springs, damagedSpringFreqs = line.split()
        unfoldedSprings = ''.join(['?' + springs] * 5)
        unfoldedSprings = unfoldedSprings[1:]
        unfoldedSprings = re.sub('\.+' ,'.' , unfoldedSprings) # every repeated . is irrelevant to solving the problem and only adds to recursion depth
        unfoldedSprings = re.sub('^\.|\.$', '', unfoldedSprings)
        new_lines.append(unfoldedSprings + ' ' + ','.join([damagedSpringFreqs] * 5))
      
      for i, line in enumerate(new_lines):
        f.write(line)
        if i != len(new_lines)-1:
          f.write('\n')

    with open("input2.txt", "r") as f:
      self.input2 = f.read().split("\n")
  
  def p1(self):

    sumArrangements = 0

    for line in self.input:
      springs, damagedSpringFreqs = line.split()
      damagedSpringFreqs = [int(freq) for freq in damagedSpringFreqs.split(",")]

      n = len(springs)
      m = len(damagedSpringFreqs)

      # index of damagedSpringFreqs, index for springs, counter holding damaged springs in a row

      # if we meet the number of damagedSpringFreqs at that index gap check (return 0 if invalid) then increment

      # finally if we reach the end of the damagedSpringFreqs array we still must continue to find no more damaged springs
      # to return 1 valid way of arranging the springs

      def backtrackWays(springIndex, damagedIndex, streak):
        if damagedIndex == m:
          if springIndex >= n or all([springs[i] != '#' for i in range(springIndex, n)]):
            return 1
          return 0
        if springIndex >= n or streak > damagedSpringFreqs[damagedIndex]:
          return 0

        if springs[springIndex] == '#':
          if streak + 1 == damagedSpringFreqs[damagedIndex]:
            if springIndex + 1 == n or springs[springIndex + 1] != '#':
              return backtrackWays(springIndex + 2, damagedIndex + 1, 0)
            return 0
          else:
            return backtrackWays(springIndex + 1, damagedIndex, streak + 1)
        
        elif springs[springIndex] == '.':
          if streak > 0:
            return 0
          return backtrackWays(springIndex + 1, damagedIndex, 0)
        
        elif springs[springIndex] == '?':
          if streak + 1 == damagedSpringFreqs[damagedIndex] and (springIndex + 1 == n or springs[springIndex + 1] != '#'):
            numWays = backtrackWays(springIndex + 2, damagedIndex + 1, 0)
            if streak == 0:
              numWays += backtrackWays(springIndex + 1, damagedIndex, streak)
            return numWays
          elif streak > 0:
            return backtrackWays(springIndex + 1, damagedIndex, streak + 1)
          elif streak == 0:
            return (
              backtrackWays(springIndex + 1, damagedIndex, streak) +
              backtrackWays(springIndex + 1, damagedIndex, streak + 1)
            )

      numWays = backtrackWays(0, 0, 0)
      sumArrangements += numWays

    print("p1", sumArrangements)

  def p2(self):

    # what can we assert to prune branches of the backtracking?

    # 1. if we keep sum of remaining damaged springs and length of line,
    # we could assert that we need a minimum space remaining before considering this a valid way removing some computation

    sumArrangements = 0

    for line in self.input2:
      springs, damagedSpringFreqs = line.split()
      damagedSpringFreqs = [int(freq) for freq in damagedSpringFreqs.split(",")]

      n = len(springs)
      m = len(damagedSpringFreqs)

      @functools.cache # same function made computationally efficient by memoization
      def backtrackWays(springIndex, damagedIndex, streak):

        if damagedIndex == m:
          if springIndex >= n or all([springs[i] != '#' for i in range(springIndex, n)]):
            return 1
          return 0
        if springIndex >= n or streak > damagedSpringFreqs[damagedIndex]:
          return 0

        if springs[springIndex] == '#':
          if streak + 1 == damagedSpringFreqs[damagedIndex]:
            if springIndex + 1 == n or springs[springIndex + 1] != '#':
              return backtrackWays(springIndex + 2, damagedIndex + 1, 0)
            return 0
          else:
            return backtrackWays(springIndex + 1, damagedIndex, streak + 1)
        
        elif springs[springIndex] == '.':
          if streak > 0:
            return 0
          return backtrackWays(springIndex + 1, damagedIndex, 0)
        
        elif springs[springIndex] == '?':
          if streak + 1 == damagedSpringFreqs[damagedIndex] and (springIndex + 1 == n or springs[springIndex + 1] != '#'):
            numWays = backtrackWays(springIndex + 2, damagedIndex + 1, 0)
            if streak == 0:
              numWays += backtrackWays(springIndex + 1, damagedIndex, streak)
            return numWays
          elif streak > 0:
            return backtrackWays(springIndex + 1, damagedIndex, streak + 1)
          elif streak == 0:
            return (
              backtrackWays(springIndex + 1, damagedIndex, streak) +
              backtrackWays(springIndex + 1, damagedIndex, streak + 1)
            )

      numWays = backtrackWays(0, 0, 0)
      sumArrangements += numWays

    print("p2", sumArrangements)

d12 = Day12()
d12.p1()
d12.p2()