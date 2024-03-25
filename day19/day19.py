from math import prod

class Day19:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read()
    with open("example.txt", "r") as f:
      self.example = f.read()

  def p1(self):

    workflowBlock, ratings = self.input.split("\n\n")

    self.workflows = {}

    def workflowMachine(conditions, part):

      for condition in conditions.split(","):
        ltIndex = condition.find('<')
        gtIndex = condition.find('>')
        colonIndex = condition.find(':')
        
        if ltIndex > -1:
          key = condition[:ltIndex]
          num = condition[ltIndex+1:colonIndex]
          if part[key] < int(num):
            return condition[colonIndex+1:]
        elif gtIndex > -1:
          key = condition[:gtIndex]
          num = condition[gtIndex+1:colonIndex]
          if part[key] > int(num):
            return condition[colonIndex+1:]
        else:
          return condition

    for workflow in workflowBlock.split("\n"):
      name, conditions = workflow.split("{")
      self.workflows[name] = conditions[:-1]

    parts = []

    for line in ratings.split("\n"):
      part = {}

      for rating in line[1:-1].split(","):
        prop, num = rating.split("=")
        part[prop] = int(num)
      parts.append(part)

    sumXmasRatings = 0

    for part in parts:
      currentWorkflow = 'in'

      while not (currentWorkflow == 'A' or currentWorkflow == 'R'):
        nextWorkflow = workflowMachine(self.workflows[currentWorkflow], part)
        currentWorkflow = nextWorkflow

      if currentWorkflow == 'A':
        sumXmasRatings += sum([val for val in part.values()])

    print("p1", sumXmasRatings)

  def p2(self):

    # Multiple node leading to 'A'
    # 1. traverse from 'in' to 'A' collapsing rating ranges/branching when multiple conditions and ending when reached 'A' or 'R'

    # 2. We will need some way of resolving when rating ranges from 'in' are overlapping so we don't double count
    # i.e. merge interval if partial overlap

    # 3. After that, for each valid range, we multiply their intervals:
    # for every x value they can have every valid m, a or s value and sum the result of every range

    workflowQ = [('in', (1, 4000, 1, 4000, 1, 4000, 1, 4000))]

    ratingToIndex = {
      'x': 0,
      'm': 2,
      'a': 4,
      's': 6
    }

    parts = []

    # "The first rule that matches the part being considered is applied immediately"
    # So constrict range on every successive condition
    # to reach the 2nd condition, the first must have been avoided e.t.c.
    # ... to reach the last fallthrough all other conditions must have be avoided

    while workflowQ:

      nextLevel = []

      for name, ratings in workflowQ:

        if any([ratings[i] > ratings[i + 1] for i in range(0, 7, 2)]):
          continue
        if name == 'R':
          continue
        if name == 'A':
          parts.append(ratings)
          continue

        ratingList = list(ratings)

        conditions = self.workflows[name]
        conditionList = conditions.split(",")

        for condition in conditionList[:-1]:

          ltIndex = condition.find('<')
          gtIndex = condition.find('>')
          colonIndex = condition.find(':')

          if ltIndex > -1:
            rating = condition[:ltIndex]
            ratingIndex = ratingToIndex[rating]
            num = int(condition[ltIndex+1:colonIndex])
            start, end = ratingList[ratingIndex], ratingList[ratingIndex + 1]
            newEnd = min(end, num - 1)

            # branch here narrowing the range to where the current condition is met
            ratingList[ratingIndex + 1] = newEnd
            nextLevel.append((condition[colonIndex+1:], tuple(ratingList)))

            # reset range and modify range to satisfy inverse of the current condition
            # so that the range falls through to the next condition
            ratingList[ratingIndex] = max(ratingList[ratingIndex], num)
            ratingList[ratingIndex + 1] = end

          elif gtIndex > -1:
            rating = condition[:gtIndex]
            ratingIndex = ratingToIndex[rating]
            num = int(condition[gtIndex+1:colonIndex])
            start, end = ratingList[ratingIndex], ratingList[ratingIndex + 1]
            newStart = max(start, num + 1)

            ratingList[ratingIndex] = newStart
            nextLevel.append((condition[colonIndex+1:], tuple(ratingList)))

            ratingList[ratingIndex] = start
            ratingList[ratingIndex + 1] = min(ratingList[ratingIndex + 1], num)

        # once inverse of all conditions is applied to the range, we reach last fallthrough
        if all([ratingList[i] < ratingList[i + 1] for i in range(0, 7, 2)]):
          nextLevel.append((conditionList[-1], tuple(ratingList)))

      workflowQ = nextLevel

    ratingCombinations = 0
    for part in parts:
      ratingCombinations += prod([part[i + 1] - part[i] + 1 for i in range(0, 7, 2)])
    print('p2', ratingCombinations)

    # step 2 was not needed, all combinations of ratings leading to Accepted are already distinct

d19 = Day19()
d19.p1()
d19.p2()