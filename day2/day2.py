class Day2:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")

    self.colorDict = {
      'red': 0,
      'green': 1,
      'blue': 2
    }
  
  def p1(self):

    maxBag = [12, 13, 14] # RBG

    def gameIsPossible(game):
      bags = game.split(": ")[1].split("; ")
      for bag in bags:
        bag = bag.split(", ")
        for cube in bag:
          strFreq, color = cube.split(" ")
          freq = int(strFreq)
          index = self.colorDict[color]
          if freq > maxBag[index]:
            return False
      return True

    sumIDs = 0
    for i, game in enumerate(self.input):
      if gameIsPossible(game):
        sumIDs += i+1
    print('p1', sumIDs)

  def p2(self):

    def getPower(game):
      minBag = [float("-inf")] * 3
      bags = game.split(": ")[1].split("; ")
      for bag in bags:
        bag = bag.split(", ")
        for cube in bag:
          strFreq, color = cube.split(" ")
          freq = int(strFreq)
          index = self.colorDict[color]
          minBag[index] = max(minBag[index], freq)
      power = 1
      for minCube in minBag:
        power *= minCube
      return power
    
    sumPowers = 0
    for game in self.input:
      sumPowers += getPower(game)
    print("p2", sumPowers)

d2 = Day2()
d2.p1()
d2.p2()