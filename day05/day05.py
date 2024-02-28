from bisect import bisect_left, bisect_right

class Day5:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n\n")

  def p1(self):
    seeds, maps = self.input[0].split(": ")[1].split(), self.input[1:]
    mapIntervals = []
    for i, mapList in enumerate(maps):
      mapList = mapList.split(":\n")[1].split("\n")
      mapIntervals.append([])
      for line in mapList:
        dstStart, srcStart, rangeLen = line.split()
        dstStart = int(dstStart)
        srcStart = int(srcStart)
        rangeLen = int(rangeLen)
        srcEnd = rangeLen - 1 + srcStart
        mapIntervals[i].append([srcStart, srcEnd, dstStart])
      mapIntervals[i].sort()

    minLocation = float("inf")
    for seed in seeds:
      src = int(seed)
      for intervals in mapIntervals:
        for interval in intervals:
          srcStart, srcEnd, dstStart = interval
          if srcStart <= src <= srcEnd:
            src = dstStart + (src - srcStart)
            break
      minLocation = min(minLocation, src)
    print("p1", minLocation)

  def p2(self):
    seeds, maps = self.input[0].split(": ")[1].split(), self.input[1:]

    seedIntervals = []
    for i in range(0, len(seeds), 2):
      start, length = int(seeds[i]), int(seeds[i+1])
      end = start + length
      seedIntervals.append([start, end])
    seedIntervals.sort()

    mapIntervals = []
    for i, mapList in enumerate(maps):
      mapList = mapList.split(":\n")[1].split("\n")
      mapIntervals.append([])
      for line in mapList:
        dstStart, srcStart, rangeLen = line.split()
        rangeLen = int(rangeLen)
        dstStart = int(dstStart)
        srcStart = int(srcStart)
        dstEnd = rangeLen - 1 + dstStart
        srcEnd = rangeLen - 1 + srcStart
        mapIntervals[i].append([dstStart, dstEnd, srcStart, srcEnd])
      mapIntervals[i].sort() # sorted by dstStart

    def findLowestSeedNum(mapIndex, lowestNum, highestNum):
      if lowestNum > highestNum:
        return
      if mapIndex == -1:
        for seedRange in seedIntervals:
          if lowestNum > seedRange[1] or highestNum < seedRange[0]:
            continue
          if lowestNum < seedRange[0]:
            return seedRange[0]
          return max(lowestNum, seedRange[0])
        return

      curMap = mapIntervals[mapIndex] # dstStart, dstEnd, srcStart, srcEnd
      n = len(curMap)

      if lowestNum < curMap[0][0]:
        seedNum = findLowestSeedNum(mapIndex-1, lowestNum, min(curMap[0][0]-1, highestNum))
        if seedNum:
          return seedNum

      for i, interval in enumerate(curMap):

        dstStart, dstEnd, srcStart, srcEnd = interval
        dstToStart = srcStart - dstStart

        if lowestNum <= dstEnd and highestNum >= dstStart:
          seedNum = findLowestSeedNum(mapIndex-1, max(dstStart, lowestNum) + dstToStart, min(dstEnd, highestNum) + dstToStart)
          if seedNum:
            return seedNum

        if i + 1 < n:
          nextIntervalDstStart = curMap[i+1][0]
          if lowestNum < nextIntervalDstStart and highestNum > dstEnd:
            seedNum = findLowestSeedNum(mapIndex-1, max(dstEnd + 1, lowestNum), min(nextIntervalDstStart-1, highestNum))
            if seedNum:
              return seedNum

      if highestNum > curMap[n-1][1]:
        seedNum = findLowestSeedNum(mapIndex-1, max(lowestNum, curMap[n-1][1] + 1), highestNum)
        if seedNum:
            return seedNum

    n = len(mapIntervals)

    locations = mapIntervals[n-1]
    lenLocations = len(locations)
    lowestLocation = 0
    locationIndex = 0
    while locationIndex < lenLocations: # consider next lowest location number as candidate
      if locations[locationIndex][0] == lowestLocation:
        seedNum = findLowestSeedNum(n-1, locations[locationIndex][0], locations[locationIndex][1])
        lowestLocation = locations[locationIndex][1] + 1
        locationIndex += 1
      else:
        seedNum = findLowestSeedNum(n-1, lowestLocation, locations[locationIndex][0]-1)
        lowestLocation = locations[locationIndex][0]
      if seedNum:
        break

    # finally translate seed number into location number

    def seedToLocation(seedNum):
      curNum = seedNum
      for i in range(n):
        curMap = sorted(mapIntervals[i], key=lambda x: x[2])
        # dstStart, dstEnd, srcStart, srcEnd = curMap[j]
        if curNum < curMap[0][2] or curNum > curMap[-1][3]: # fall through
          continue
        for j in range(len(curMap)):
          if curMap[j][2] <= curNum <= curMap[j][3]:
            curNum = curNum + curMap[j][0] - curMap[j][2]
            break
          if j + 1 < len(curMap) and curMap[j][3] < curNum < curMap[j+1][2]: # fall through
            break
      return curNum

    print("p2", seedToLocation(seedNum))

d5 = Day5()
d5.p1()
d5.p2()