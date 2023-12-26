import functools
from collections import Counter

class Day7:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")

  def isFullHouse(self, frequencies):
    return frequencies[0] == 3 and frequencies[1] == 2

  def isTwoPair(self, frequencies):
    return frequencies[0] == 2 and frequencies[1] == 2

  def p1(self):

    def getHandStrength(hand):
      counter = Counter(hand)
      frequencies = sorted(counter.values(), reverse=True)
      for freq in frequencies:
        if freq == 5:
          return 6
        if freq == 4:
          return 5
        if freq == 3:
          if self.isFullHouse(frequencies):
            return 4
          return 3        
        if freq == 2:
          if self.isTwoPair(frequencies):
            return 2
          return 1
        return 0

    cardValues = {
      "A": 13,
      "K": 12,
      "Q": 11,
      "J": 10,
      "T": 9,
      "9": 8,
      "8": 7,
      "7": 6,
      "6": 5,
      "5": 4,
      "4": 3,
      "3": 2,
      "2": 1
    }

    def compare(a, b):
      handA, handB = a[:5], b[:5]
      aStrength, bStrength = getHandStrength(handA), getHandStrength(handB)

      if aStrength < bStrength:
        return -1
      elif aStrength > bStrength:
        return 1
      else:
        for i in range(5):
          cardA, cardB = handA[i], handB[i]
          if cardValues[cardA] < cardValues[cardB]:
            return -1
          elif cardValues[cardA] > cardValues[cardB]:
            return 1
    
      print("should be unreachable")
      return 0

    self.input.sort(key=functools.cmp_to_key(compare))

    print("p1", sum([(i+1) * int(line[6:]) for i, line in enumerate(self.input)]))

  def p2(self):

    def getHandStrength(hand):
      counter = Counter(hand)
      frequencies = sorted(counter.values(), reverse=True)
      freqJ = counter['J']
      if freqJ:
        sortedKeyVals = sorted(counter.items(), key=lambda x: -x[1])
        
        # sort hands by card frequency
        if sortedKeyVals[0][1] > 3: # 5 of a kind
          return 6
        if sortedKeyVals[0][1] == 3:
          if len(sortedKeyVals) == 2: # Only 2 types of card + one is guaranteed a Joker, 5 of a kind
            return 6
          return 5 # 3 types of card + 1 Joker, 4 of a kind
        if sortedKeyVals[0][1] == 2:
          
          if len(sortedKeyVals) == 3:
            if freqJ == 1:
              return 4 # Full House > three of a kind
            else: # freqJ is 2
              return 5 # 4 of a kind

          # never make 2 pair over three of a kind: JJ--- or 22---
          return 3 # three of a kind

        return 1
      else:
        if frequencies[0] == 5:
          return 6
        if frequencies[0] == 4:
          return 5
        if frequencies[0] == 3:
          if self.isFullHouse(frequencies):
            return 4
          return 3        
        if frequencies[0] == 2:
          if self.isTwoPair(frequencies):
            return 2
          return 1
        return 0

    cardValues = {
      "A": 13,
      "K": 12,
      "Q": 11,
      "T": 10,
      "9": 9,
      "8": 8,
      "7": 7,
      "6": 6,
      "5": 5,
      "4": 4,
      "3": 3,
      "2": 2,
      "J": 1,
    }

    def compare(a, b):
      handA, handB = a[:5], b[:5]
      aStrength, bStrength = getHandStrength(handA), getHandStrength(handB)

      if aStrength < bStrength:
        return -1
      elif aStrength > bStrength:
        return 1
      else:
        for i in range(5):
          cardA, cardB = handA[i], handB[i]
          if cardValues[cardA] < cardValues[cardB]:
            return -1
          elif cardValues[cardA] > cardValues[cardB]:
            return 1
      
      print("should be unreachable")
      return 0

    self.input.sort(key=functools.cmp_to_key(compare))

    print("p2", sum([(i+1) * int(line[6:]) for i, line in enumerate(self.input)]))

d7 = Day7()
d7.p1()
d7.p2()