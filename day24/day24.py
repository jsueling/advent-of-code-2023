class Day24:

  def __init__(self):
    with open("input.txt", "r") as f:
      self.input = f.read().split("\n")
    with open("example.txt", "r") as f:
      self.example = f.read().split("\n")
  
  def p1(self):

    # find x, y of intersection for each pair of hailstones
    # if intersection is inside boundaries x,y: 200000000000000, 400000000000000
    # and intersection lies in the path of each hailstone

    # y = 22.5 - 0.5x
    # y = 1 + x

    # 1 + x = 22.5 - 0.5x
    # 1.5x = 21.5
    # x = 21.5 / 1.5

    hailstones = []

    for line in self.input:
      positions, velocities = line.split("@")
      positions = [int(pos) for pos in positions.strip().split(", ")]
      velocities = [int(vel) for vel in velocities.strip().split(", ")]

      xVel, yVel, _ = velocities
      xPos, yPos, _ = positions

      hailstones.append([xPos, yPos, xVel, yVel])
    
    def isInPath(endX, endY, hailstone):

      startX, startY, xVel, yVel = hailstone

      return (xVel > 0 and endX > startX) or (xVel < 0 and endX < startX)

    intersections = 0

    for i in range(len(hailstones)):

      x1, y1, vx1, vy1 = hailstones[i]

      slope1 = vy1 / vx1

      intercept1 = y1 - x1 * slope1

      for j in range(i+1, len(hailstones)):

        x2, y2, vx2, vy2 = hailstones[j]

        slope2 = vy2 / vx2

        intercept2 = y2 - x2 * slope2

        if slope1 == slope2:
          continue

        x = (intercept2 - intercept1) / (slope1 - slope2)

        y = slope1 * x + intercept1

        minRange, maxRange = 200000000000000, 400000000000000

        if minRange <= x <= maxRange and minRange <= y <= maxRange and isInPath(x, y, hailstones[i]) and isInPath(x, y, hailstones[j]):
          intersections += 1

    print("p1", intersections)

  def p2(self):

    # the line must pass through every hailstone path

    # find lines that pass through every hailstone path

    # find a set of possible positions and velocities (lines)

    # test the validity of each line

    # sort by distance to collision, check time is increasing in collision time

    # ----------------------------------------

    # Credits to Werner for his solution:
    # https://youtu.be/nP2ahZs40U8?si=TUBdYjzJ_eF_03ad
    # https://github.com/werner77/AdventOfCode/blob/master/src/main/kotlin/com/behindmedia/adventofcode/year2023/day24/Day24.kt
 
    # We assume the rock to be stationary and subtract each hailstone's velocity by the rock's velocity,
    # We brute force the rock's integer velocity combinations and test them such that each hailstone's new path now points at the rock
    # The rock's implied position is at the intersection of each pair of updated hailstones (if they intersect at all)
    # If all the pairs share one intersection point for a given velocity we have found the position and the velocity of the rock throw

    hailstones = []

    for line in self.input:
      positions, velocities = line.split("@")
      positions = [int(pos) for pos in positions.strip().split(", ")]
      velocities = [int(vel) for vel in velocities.strip().split(", ")]

      hailstones.append([*positions, *velocities])
    
    n = len(hailstones)

    def getRockPosition(vx, vy, vz):

          collisions = 0

          intersections = set()

          for i in range(len(hailstones)):

            px1, py1, pz1, vx1, vy1, vz1 = hailstones[i]

            vx1 -= vx
            vy1 -= vy
            vz1 -= vz

            for j in range(i+1, len(hailstones)):

              px2, py2, pz2, vx2, vy2, vz2 = hailstones[j]

              vx2 -= vx
              vy2 -= vy
              vz2 -= vz

              # with help from Radford Mathematics: https://youtu.be/N-qUfr-rz_Y?si=HrFDthyBom4oz5eu

              # x = px1 + a * vx1
              # y = py1 + a * vy1
              # z = pz1 + a * vz1

              # x = px2 + b * vx2
              # y = py2 + b * vy2
              # z = pz2 + b * vz2

              # 1. px1 + a * vx1 = px2 + b * vx2
              # 2. py1 + a * vy1 = py2 + b * vy2
              # 3. pz1 + a * vz1 = pz2 + b * vz2

              # b * vx2 - a * vx1 = px1 - px2
              # b = (px1 - px2 + a * vx1) / vx2

              # sub b into 2.

              # 2. py1 + a * vy1 = py2 + vy2 * b

              # py1 + a * vy1 = py2 + vy2 * (px1 - px2 + a * vx1) / vx2
              # vx2 * py1 + vx2 * a * vy1 = vx2 * py2 + vy2 * px1 - vy2 * px2 + vy2 * a * vx1
              # a * (vx2 * vy1 - vy2 * vx1) = vx2 * py2 - vx2 * py1 + vy2 * px1 - vy2 * px2
              # a = (vx2 * py2 - vx2 * py1 + vy2 * px1 - vy2 * px2) / (vx2 * vy1 - vy2 * vx1)

              # a = (vx2 * (py2 - py1) + vy2 * (px1 - px2)) / (vx2 * vy1 - vy2 * vx1)

              # find b using: b = (px1 - px2 + a * vx1) / vx2
              
              if vx2 * vy1 == vy2 * vx1 or vx2 == 0:
                return

              a = (vx2 * (py2 - py1) + vy2 * (px1 - px2)) / (vx2 * vy1 - vy2 * vx1)
              b = (px1 - px2 + a * vx1) / vx2

              # verify in 3. for the given a and b that: pz1 + a * zy1 == pz2 + b * vz2

              if pz1 + a * vz1 != pz2 + b * vz2:
                return
              
              x = px1 + a * vx1
              y = py1 + a * vy1
              z = pz1 + a * vz1

              intersections.add((x, y, z))

              collisions += 1

              if len(intersections) > 1:
                return

              # We could test that all hailstones collide at one point
              # but we consider it unlikely so loosen condition to save time
              # if collisions == n * (n-1) / 2:

              if collisions > 1:
                return list(intersections)[0]

    searchRange = 300

    for vx in range(-searchRange, searchRange):
      for vy in range(-searchRange, searchRange):
        for vz in range(-searchRange, searchRange):
          result = getRockPosition(vx, vy, vz)
          if result is not None:
            print("p2", sum(result), result, vx, vy, vz)
            return

d24 = Day24()
d24.p1()
d24.p2()