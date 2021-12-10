#!/usr/bin/env python3

data = [x.strip() for x in open('data.txt').readlines()]
CARDINAL_ONLY = False

class Line():

  def __init__(self, x1, y1, x2, y2):
    self.x1 = int(x1)
    self.y1 = int(y1)
    self.x2 = int(x2)
    self.y2 = int(y2)

  def isVertical(self):
    return self.x1 == self.x2

  def isHorizontal(self):
    return self.y1 == self.y2

  def isCardinal(self):
    return self.isHorizontal() or self.isVertical()

  def allPoints(self):
    if self.isHorizontal():
      allY = self.y1
      return [(x, allY) for x in range(min(self.x1, self.x2), max(self.x1, self.x2)+1)]

    if self.isVertical():
      allX = self.x1
      return [(allX, y) for y in range(min(self.y1, self.y2), max(self.y1, self.y2)+1)]

    # is diagonal
    # will always be at a 45 degree angle
    deltaX = 1 if self.x1 < self.x2 else -1
    deltaY = 1 if self.y1 < self.y2 else -1

    currentX, currentY = self.x1, self.y1

    points = []
    while currentX != self.x2:
      points.append((currentX, currentY))
      currentX += deltaX
      currentY += deltaY
    points.append((self.x2, self.y2))

    return points

lines = []

for l in data:
  start, end = l.split(' -> ')
  x1, y1 = start.split(',')
  x2, y2 = end.split(',')
  newLine = Line(x1, y1, x2, y2)
  if not CARDINAL_ONLY or newLine.isCardinal():
    lines.append(newLine)

pointsCount = {}

for line in lines:
  for point in line.allPoints():
    pointsCount[point] = pointsCount.get(point, 0) + 1

overlaps = [point for point in pointsCount.keys() if pointsCount[point] >= 2]

print(f'Total overlaps: {len(overlaps)}')
