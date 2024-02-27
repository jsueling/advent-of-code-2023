from collections import defaultdict

class Node:

  def __init__(self, prev, nxt, label='dummy', focalLength=0): # double linked list
    self.prev = prev
    self.nxt = nxt
    self.label = label
    self.focalLength = focalLength

class Box:

  def __init__(self):
    self.first = Node(None, None)
    self.prev = Node(None, self.first)
    self.first.prev = self.prev

  def remove(self, label):

    prev, cur = self.prev, self.first
    while cur.nxt and cur.label != label: # progress to end of list or found label
      cur = cur.nxt
      prev = prev.nxt
    
    if cur.label == label:
      if not cur.nxt:
        prev.nxt = None
      else:
        nxtNode = cur.nxt
        prev.nxt, nxtNode.prev = nxtNode, prev

    if cur.label == "dummy":
      return 1 # flag to show the Box is empty and can be safely deleted from boxes defaultdict
    return 0

  def add(self, label, focalLength):

    cur = self.first
    while cur.nxt and cur.label != label:
      cur = cur.nxt
    
    if cur.label == label:
      cur.focalLength = focalLength
    elif not cur.nxt:
      cur.nxt = Node(cur, None, label, focalLength)

  def getFocusingPower(self, boxIndex):
    focusingPower = 0
    cur = self.first
    slotNum = 0
    while cur.nxt:
      cur = cur.nxt
      slotNum += 1
      focusingPower += slotNum * cur.focalLength
    focusingPower *= (boxIndex + 1)
    return focusingPower

class Day15:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split(",")
    with open("example.txt", "r") as f:
      self.example = f.read().split(",")

  def getBoxNum(self, string):
      currentValue = 0
      for character in string:
        currentValue += ord(character)
        currentValue *= 17
        currentValue %= 256
      return currentValue

  def p1(self):

    sumResults = 0
    for string in self.input:
      sumResults += self.getBoxNum(string)
    print("p1", sumResults)

  def p2(self):

    boxes = defaultdict(lambda: Box()) # credits to https://gist.github.com/poros/04a368f465e3c69d8d55

    for string in self.input:

      if string[-1].isnumeric():
        label, focalLength = string[:-2], int(string[-1])
        boxNum = self.getBoxNum(label)
        boxes[boxNum].add(label, focalLength)
      else:
        label = string[:-1]
        boxNum = self.getBoxNum(label)
        if boxNum in boxes:
          result = boxes[boxNum].remove(label)
          if result == 1:
            del boxes[boxNum] # save some time looking up and computing empty boxes

    print("p2", sum([box.getFocusingPower(key) for key, box in boxes.items()]))

d15 = Day15()
d15.p1()
d15.p2()