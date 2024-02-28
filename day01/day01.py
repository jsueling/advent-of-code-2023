class Day1:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")
  
  def p1(self):
    sumCalibrationValues = 0
    for line in self.input:
      numerics = [char for char in line if char.isnumeric()]
      calibrationString = numerics[0] + numerics[-1]
      sumCalibrationValues += int(calibrationString)
    print("p1", sumCalibrationValues)
  
  def p2(self):

    numDict = {
      'one': '1',
      'two': '2',
      'three': '3',
      'four': '4',
      'five': '5',
      'six': '6',
      'seven': '7',
      'eight': '8',
      'nine': '9'
    }

    def findFirstNumeric(line):
      n = len(line)
      for i in range(n):
        if line[i].isnumeric():
          return line[i]
        else:
          for strWord, strDigit in numDict.items():
            if i + len(strWord) < n and line[i:i+len(strWord)] == strWord:
              return strDigit

    def findLastNumeric(line):
      n = len(line)
      for i in range(n-1,-1,-1):
        if line[i].isnumeric():
          return line[i]
        else:
          for strWord, strDigit in numDict.items():
            if i - len(strWord) + 1 >= 0 and line[i-len(strWord)+1:i+1] == strWord:
              return strDigit

    sumCalibrationValues = 0
    for line in self.input:
      calibrationString = findFirstNumeric(line) + findLastNumeric(line)
      sumCalibrationValues += int(calibrationString)        
    print("p2", sumCalibrationValues)

d1 = Day1()
d1.p1()
d1.p2()