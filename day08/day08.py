from collections import defaultdict
from math import lcm

class Day8:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")

    self.instructions, self.network = self.input[0], self.input[2:]

    self.nodeToIndex = {}
    self.networkList = []

    self.aIndices = []
    self.zIndices = set()

    for i, line in enumerate(self.network):
      source = line[:3]
      self.nodeToIndex[source] = i

    for i, line in enumerate(self.network):
      source = line[:3]
      left, right = line[7:10], line[12:15]
      self.networkList.append([self.nodeToIndex[left], self.nodeToIndex[right]])

      if line[2] == 'A':
        self.aIndices.append(i)
      if line[2] == 'Z':
        self.zIndices.add(i)

    self.directions = []
    for direction in self.instructions:
      if direction == 'L':
        self.directions.append(0)
      else:
        self.directions.append(1)

  def p1(self):
    node = self.nodeToIndex['AAA']
    zzz = self.nodeToIndex['ZZZ']
    steps = 0
    while True:
      if node == zzz:
        print("p1", steps)
        return
      i = steps % len(self.directions)
      node = self.networkList[node][self.directions[i]]
      steps += 1

  def p2(self):

    curNodes = self.aIndices[:]
    reachable = defaultdict(set)
    loopRecord = defaultdict(list)
    steps = 0
    n = len(curNodes)
    while steps < 1000000:
      zNodes = 0
      direction = steps % len(self.directions)
      steps += 1
      for i in range(n):
        curNodes[i] = self.networkList[curNodes[i]][self.directions[direction]]
        if curNodes[i] in self.zIndices:
          zNodes += 1
          a, z = self.network[self.aIndices[i]][:3], self.network[curNodes[i]][:3]

          reachable[a].add(z)

          if len(loopRecord[a]) == 4:
            continue

          loopRecord[a].append(steps)

      if zNodes == n:
        print("p2", steps)
        return

    for start in reachable:
      print(start, reachable[start])
      # This shows that each start node has a unique end node in it's own contained loop
      # HMA {'QLZ'}
      # CXA {'NVZ'}
      # NPA {'DHZ'}
      # VHA {'KQZ'}
      # GQA {'BJZ'}
      # AAA {'ZZZ'}

    stepsInLoop = []

    for zFound in loopRecord:
      print(zFound, loopRecord[zFound], loopRecord[zFound][3] - loopRecord[zFound][2], loopRecord[zFound][2] - loopRecord[zFound][1], loopRecord[zFound][1] - loopRecord[zFound][0])
      # This shows that each Z node repeats every X steps
      # HMA [13771, 27542, 41313, 55084] 13771 13771 13771
      # CXA [17287, 34574, 51861, 69148] 17287 17287 17287
      # NPA [19631, 39262, 58893, 78524] 19631 19631 19631
      # VHA [20803, 41606, 62409, 83212] 20803 20803 20803
      # GQA [21389, 42778, 64167, 85556] 21389 21389 21389
      # AAA [23147, 46294, 69441, 92588] 23147 23147 23147
      stepsInLoop.append(loopRecord[zFound][2] - loopRecord[zFound][1])

    print("p2", lcm(*stepsInLoop))

d8 = Day8()
d8.p1()
d8.p2()