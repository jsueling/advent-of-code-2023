class Day9:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")

  def p1(self):

    sumExtrapolated = 0

    for line in self.input:
      numList = [int(num) for num in line.split()]

      diff = [(numList[i] - numList[i-1]) for i in range(1, len(numList))]
      lastDiffs = [diff[-1]]

      while not all([(d == 0) for d in diff]):
        diff = [(diff[i] - diff[i-1]) for i in range(1, len(diff))]
        lastDiffs.append(diff[-1])

      extrapolated = sum(lastDiffs) + numList[-1]
      sumExtrapolated += extrapolated

    print("p1", sumExtrapolated)

  def p2(self):

    sumBackExtrapolated = 0
    for line in self.input:
      numList = [int(num) for num in line.split()]

      diff = [(numList[i] - numList[i-1]) for i in range(1, len(numList))]
      firstDiffs = [diff[0]]

      while not all([(d == 0) for d in diff]):
        diff = [(diff[i] - diff[i-1]) for i in range(1, len(diff))]
        firstDiffs.append(diff[0])

      prev = 0
      for i in range(len(firstDiffs)-2,-1,-1):
        prev = firstDiffs[i] - prev

      sumBackExtrapolated += numList[0] - prev

    print("p2", sumBackExtrapolated)

d9 = Day9()
d9.p1()
d9.p2()