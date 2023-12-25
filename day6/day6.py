class Day6:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")
  
  def p1(self):
    time = [int(t) for t in self.input[0].split()[1:]]
    distance = [int(d) for d in self.input[1].split()[1:]]

    n = len(time)
    numWays = 1

    for raceIndex in range(n):
      curWays = 0
      distRecord = distance[raceIndex]
      maxTime = time[raceIndex]
      for held in range(1, maxTime):
        speed = held
        remainingTime = maxTime - held
        if remainingTime * speed > distRecord:
          curWays += 1
      numWays *= curWays
    print("p1", numWays)

  def p2(self): # Binary search to find lower and upper bounds

    time = int("".join(self.input[0].split()[1:]))
    distance = int("".join(self.input[1].split()[1:]))

    def boatWinsRace(secondsHeld):
      remainingTime = time - secondsHeld
      return remainingTime * secondsHeld > distance
    
    guesstimate = time // 2
    print(boatWinsRace(guesstimate)) # guess midpoint, returned true

    # use to set up 2 binary searches to find boundaries

    def getMinHeld(l, r):
      while l <= r:
        m = (l + r) // 2

        mWins, mPlusOneWins = boatWinsRace(m), boatWinsRace(m+1)

        if not mWins and mPlusOneWins:
          return m + 1
        
        elif mWins and mPlusOneWins:
          r = m - 1
        
        elif not mWins and not mPlusOneWins:
          l = m + 1
      
    def getMaxHeld(l, r):

      while l <= r:
        m = (l + r) // 2

        mWins, mPlusOneWins = boatWinsRace(m), boatWinsRace(m+1)

        if mWins and not mPlusOneWins:
          return m
        
        elif mWins and mPlusOneWins:
          l = m + 1
        
        elif not mWins and not mPlusOneWins:
          r = m - 1

    minPossibleHeld, maxPossibleHeld = getMinHeld(1, guesstimate), getMaxHeld(guesstimate, time-1)

    print("p2", maxPossibleHeld - minPossibleHeld + 1)

d6 = Day6()
d6.p1()
d6.p2()