#!/usr/bin/env python3
class Cuboid():
  def __init__(self, on, coords=None, literals=None):
    self.on = on
    if coords:
      x,y,z = coords.split(',')
      self.minX, self.maxX = (int(num) for num in x[2:].split('..'))
      self.minY, self.maxY = (int(num) for num in y[2:].split('..'))
      self.minZ, self.maxZ = (int(num) for num in z[2:].split('..'))
    else:
      self.minX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ = literals
    self.overlappers = []
    
  def cellIn(self, cell):
    x,y,z = cell
    return self.minX <= x <= self.maxX and self.minY <= y <= self.maxY and self.minZ <= z <= self.maxZ
  
  def overlaps(self, other):
    corners = 0
    for x in (other.minX, other.maxX):
      for y in (other.minY, other.maxY):
        for z in (other.minZ, other.maxZ):
          if self.cellIn((x,y,z)):
            corners += 1
    if corners:
      return corners
    # check self isn't wholely within other
    for x in (self.minX, self.maxX):
      for y in (self.minY, self.maxY):
        for z in (self.minZ, self.maxZ):
          if not other.cellIn((x,y,z)):
            return 0
    return 8
  
  def splitCuboid(self, overlapper, corners):
    newCuboids = set()
    if corners == 8:
      return newCuboids
    if corners == 4:
      # find out what half (6 options) return that.
      # 1 new cuboid
      # variable names is which side gets cut off
      
      # split on Y:
      top = True
      bottom = True
      for x in (self.minX, self.maxX):
        for z in (self.minZ, self.maxZ):
          if not overlapper.cellIn((x, self.maxY, z)):
            top = False
          if not overlapper.cellIn((x, self.minY, z)):
            bottom = False
      if top:
        newMaxY = overlapper.minY-1
        newCuboids.add(Cuboid(self.on, literals=(self.minX, self.maxX, self.minY, newMaxY, self.minZ, self.maxZ)))
        return newCuboids
      if bottom:
        newMinY = overlapper.maxY+1
        newCuboids.add(Cuboid(self.on, literals=(self.minX, self.maxX, newMinY, self.maxY, self.minZ, self.maxZ)))
        return newCuboids
      
      # split on X:
      left = True
      right = True
      for y in (self.minY, self.maxY):
        for z in (self.minZ, self.maxZ):
          if not overlapper.cellIn((self.minX, y, z)):
            left = False
          if not overlapper.cellIn((self.maxX, y, z)):
            right = False
      if left:
        newMinX = overlapper.maxX+1
        newCuboids.add(Cuboid(self.on, literals=(newMinX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ)))
        return newCuboids
      if right:
        newMaxX = overlapper.minX-1
        newCuboids.add(Cuboid(self.on, literals=(self.minX, newMaxX, self.minY, self.maxY, self.minZ, self.maxZ)))
        return newCuboids
      
      # split on Z:
      front = True
      back = True
      for x in (self.minX, self.maxX):
        for y in (self.minY, self.maxY):
          if not overlapper.cellIn((x, y, self.minZ)):
            back = False
          if not overlapper.cellIn((x, y, self.maxZ)):
            front = False
      if front:
        newMinZ = overlapper.minZ-1
        newCuboids.add(Cuboid(self.on, literals=(self.minX, self.maxX, self.minY, self.maxY, newMinZ, self.maxZ)))
        return newCuboids
      if back:
        newMaxZ = overlapper.maxZ+1
        newCuboids.add(Cuboid(self.on, literals=(self.minX, self.maxX, self.minY, self.maxY, self.minZ, newMaxZ)))
        return newCuboids
    
    cutCorners = self.findCutCorners(overlapper)
    if corners == 2:
      # find the cut off corners (2 adjacent from 8, 12 options)
      # return 2 new cuboids
      # if no lefts cut create left cuboid
      # if no rights cut create right cuboid
      # maybe create other cuboids, or possibly just create whatever's left and call splitCuboid again to get that bit
      pass
    if corners == 1:
      # find the missing corner (8 options)
      # return 3 new cuboids
      # create left or right cuboid
      # create top or bottom cuboid
      # creat front or back cuboid
      pass
  
  def findCutCorners(self, overlapper):
    corners = {
      'lbb': (self.minX, self.minY, self.minZ),
      'lbf': (self.minX, self.minY, self.maxZ),
      'ltb': (self.minX, self.maxY, self.minZ),
      'ltf': (self.minX, self.maxY, self.maxZ),
      'rbb': (self.maxX, self.minY, self.minZ),
      'rbf': (self.maxX, self.minY, self.maxZ),
      'rtb': (self.maxX, self.maxY, self.minZ),
      'rtf': (self.maxX, self.maxY, self.maxZ),
    }
    for code, coords in corners.items():
      if overlapper.cellIn(coords):
        corners[code] = True
      else:
        corners[code] = False
    
    return corners
    
  def cellCount(self):
    return (self.maxX+1-self.minX) * (self.maxY+1-self.minY) * (self.maxZ+1-self.minZ) - sum(o.cellCount() for o in self.overlappers)
  
  

testA = Cuboid(True, literals=(0,10,0,10,0,10))
testB = Cuboid(False, literals=(0,10,0,10,0,10))
result = list(testA.splitCuboid(testB, testB.overlaps(testA)))
print(list(result))

  
#instructions = [x.strip().split(' ') for x in open('test.txt').readlines()]
#
#cuboids = set()
#for onOff, coords in instructions:
# c = Cuboid(onOff == 'on', coords)
# 
# for o in cuboids:
#   corners = c.overlaps(o)
#   if corners:
#     cuboids.discard(o)
#     cuboids.update(o.splitCuboid(c, corners))
#       
# if c.on:
#   cuboids.add(c)
#
#print('All cells:', sum(c.cellCount() for c in cuboids))