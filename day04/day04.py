from collections import defaultdict

class Day4:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")

    self.winning = [0] * len(self.input)

  def p1(self):
    points = 0
    for i, line in enumerate(self.input):
      line = line.split(": ")[1]
      winning, own = line.split(" | ")
      winning = winning.split()
      own = own.split()
      winning = set(winning)
      power = sum([(1 if num in winning else 0) for num in own]) - 1
      self.winning[i] = power + 1
      if power > -1:
        points += 2 ** power
    print("p1", points)

  def p2(self):
    n = len(self.winning)
    # dp[i] is the how many instances of cards the i'th card will win.
    dp = defaultdict(lambda: 1) # All cards will contribute 1 instance as their original
    for i in range(n-1,-1,-1):
      for j in range(self.winning[i]):
        nextJthCard = i+j+1
        if nextJthCard < n: # (Cards will never make you copy a card past the end of the table.)
          dp[i] += dp[nextJthCard]

    print("p2", sum([dp[k] for k in range(n)]))

d4 = Day4()
d4.p1()
d4.p2()