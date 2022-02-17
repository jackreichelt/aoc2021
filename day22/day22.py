#!/usr/bin/env python3
from itertools import combinations, permutations
from sys import maxsize

class Cuboid():
  def __init__(self, on, coords=None, literals=None):
    self.on = on
    self.off = not on
    if coords:
      x,y,z = coords.split(',')
      self.minX, self.maxX = (int(num) for num in x[2:].split('..'))
      self.minY, self.maxY = (int(num) for num in y[2:].split('..'))
      self.minZ, self.maxZ = (int(num) for num in z[2:].split('..'))
    else:
      self.minX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ = literals
    self.cellCount = self.findCellCount()
    
  def __str__(self):
    return f'X:{self.minX}, {self.maxX}, Y:{self.minY}, {self.maxY}, Z: {self.minZ}, {self.maxZ}'
    
  def cellIn(self, cell):
    x,y,z = cell
    return self.minX <= x <= self.maxX and self.minY <= y <= self.maxY and self.minZ <= z <= self.maxZ
  
  def whollyWithin(self, other):
    for x in (self.minX, self.maxX):
      for y in (self.minY, self.maxY):
        for z in (self.minZ, self.maxZ):
          if not other.cellIn((x,y,z)):
            return False
    return True
  
  def splitCuboid(self, overlapper):
    cutCorners = self.findCutCorners(overlapper)
    overlapPoints = [corner for corner, cut in cutCorners.items() if cut == True]
    
    newCuboids = []
    
    if len(overlapPoints) == 8:
      if not self.whollyWithin(overlapper):
        print('error: wrongly deleting')
      return newCuboids, self.cellCount
    
    if len(overlapPoints) == 4:
      if all('r' in corner for corner in overlapPoints):
        # make left cuboid
        newMaxX = overlapper.minX-1
        newCuboids.append(Cuboid(self.on, literals=(self.minX, newMaxX, self.minY, self.maxY, self.minZ, self.maxZ)))
        voidCube = Cuboid(self.on, literals=(overlapper.minX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ))

      elif all('l' in corner for corner in overlapPoints):
        # make right cuboid
        newMinX = overlapper.maxX+1
        newCuboids.append(Cuboid(self.on, literals=(newMinX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ)))
        voidCube = Cuboid(self.on, literals=(self.minX, overlapper.maxX, self.minY, self.maxY, self.minZ, self.maxZ))

      elif all('t' in corner for corner in overlapPoints):
        # make bottom cuboid
        newMaxY = overlapper.minY-1
        newCuboids.append(Cuboid(self.on, literals=(self.minX, self.maxX, self.minY, newMaxY, self.minZ, self.maxZ)))
        voidCube = Cuboid(self.on, literals=(self.minX, self.maxX, overlapper.minY, self.maxY, self.minZ, self.maxZ))

      elif all('b' in corner for corner in overlapPoints):
        # make top cuboid
        newMinY = overlapper.maxY+1
        newCuboids.append(Cuboid(self.on, literals=(self.minX, self.maxX, newMinY, self.maxY, self.minZ, self.maxZ)))
        voidCube = Cuboid(self.on, literals=(self.minX, self.maxX, self.minY, overlapper.maxY, self.minZ, self.maxZ))
        
      elif all('f' in corner for corner in overlapPoints):
        # make back cuboid
        newMaxZ = overlapper.minZ-1
        newCuboids.append(Cuboid(self.on, literals=(self.minX, self.maxX, self.minY, self.maxY, self.minZ, newMaxZ)))
        voidCube = Cuboid(self.on, literals=(self.minX, self.maxX, self.minY, self.maxY, overlapper.minZ, self.maxZ))
        
      elif all('k' in corner for corner in overlapPoints):
        # make front cuboid
        newMinZ = overlapper.maxZ+1
        newCuboids.append(Cuboid(self.on, literals=(self.minX, self.maxX, self.minY, self.maxY, newMinZ, self.maxZ)))
        voidCube = Cuboid(self.on, literals=(self.minX, self.maxX, self.minY, self.maxY, self.minZ, overlapper.maxZ))
                
#     if any([nC.overlappedBy(voidCube) for nC in newCuboids]) or sum([nC.cellCount for nC in newCuboids]) + voidCube.cellCount != self.cellCount:
#       print('error: incorrect halving')
#     if any([nC.overlappedBy(overlapper) for nC in newCuboids]):
#       print('error: halves incorrectly positioned')
#     if not all([nC.whollyWithin(self) for nC in newCuboids]):
#       print('error: halves overflowed original')
#     if not voidCube.whollyWithin(self) or not voidCube.whollyWithin(overlapper):
#       print('error: halves void cube wrong')
      return newCuboids, voidCube.cellCount
    
    if len(overlapPoints) == 2:
      cutEdgeCubes = self.edgeCutCubeResults(overlapper, overlapPoints)
      
      for cutEdgeCube in cutEdgeCubes[:-1]:
        newCuboids.append(Cuboid(self.on, literals=cutEdgeCube))
      voidCube = Cuboid(self.on, literals=cutEdgeCubes[-1])
      
#     if any([nC.overlappedBy(voidCube) for nC in newCuboids]) or sum([nC.cellCount for nC in newCuboids]) + voidCube.cellCount != self.cellCount:
#       print('error: incorrect quarters')
#     if any([nC.overlappedBy(overlapper) for nC in newCuboids]):
#       print('error: quarters incorrectly positioned')
#     if not all([nC.whollyWithin(self) for nC in newCuboids]):
#       print('error: quarters overflowed original')
#     if not voidCube.whollyWithin(self) or not voidCube.whollyWithin(overlapper):
#       print('error: quarters void cube wrong')
      return newCuboids, voidCube.cellCount

    if len(overlapPoints) == 1:
      # find appropriate "centre" point
      newMinX, newMaxX, newMinY, newMaxY, newMinZ, newMaxZ = self.findIntersectionBoundaries(overlapper, overlapPoints[0])
            
      if 'lbk' not in overlapPoints:
        # add lbk corner cuboid
        nc = Cuboid(self.on, literals=(self.minX, newMaxX, self.minY, newMaxY, self.minZ, newMaxZ))
        newCuboids.append(nc)
      else:
        voidCube = Cuboid(self.on, literals=(self.minX, newMaxX, self.minY, newMaxY, self.minZ, newMaxZ))
      if 'lbf' not in overlapPoints:
        # add lbf corner cuboid
        nc = Cuboid(self.on, literals=(self.minX, newMaxX, self.minY, newMaxY, newMinZ, self.maxZ))
        newCuboids.append(nc)
      else:
        voidCube = Cuboid(self.on, literals=(self.minX, newMaxX, self.minY, newMaxY, newMinZ, self.maxZ))
      if 'ltk' not in overlapPoints:
        # add ltk corner cuboid
        nc = Cuboid(self.on, literals=(self.minX, newMaxX, newMinY, self.maxY, self.minZ, newMaxZ))
        newCuboids.append(nc)
      else:
        voidCube = Cuboid(self.on, literals=(self.minX, newMaxX, newMinY, self.maxY, self.minZ, newMaxZ))
      if 'ltf' not in overlapPoints:
        # add ltf corner cuboid
        nc = Cuboid(self.on, literals=(self.minX, newMaxX, newMinY, self.maxY, newMinZ, self.maxZ))
        newCuboids.append(nc)
      else:
        voidCube = Cuboid(self.on, literals=(self.minX, newMaxX, newMinY, self.maxY, newMinZ, self.maxZ))
      if 'rbk' not in overlapPoints:
        # add rbk corner cuboid
        nc = Cuboid(self.on, literals=(newMinX, self.maxX, self.minY, newMaxY, self.minZ, newMaxZ))
        newCuboids.append(nc)
      else:
        voidCube = Cuboid(self.on, literals=(newMinX, self.maxX, self.minY, newMaxY, self.minZ, newMaxZ))
      if 'rbf' not in overlapPoints:
        # add rbf corner cuboid
        nc = Cuboid(self.on, literals=(newMinX, self.maxX, self.minY, newMaxY, newMinZ, self.maxZ))
        newCuboids.append(nc)
      else:
        voidCube = Cuboid(self.on, literals=(newMinX, self.maxX, self.minY, newMaxY, newMinZ, self.maxZ))
      if 'rtk' not in overlapPoints:
        # add rtk corner cuboid
        nc = Cuboid(self.on, literals=(newMinX, self.maxX, newMinY, self.maxY, self.minZ, newMaxZ))
        newCuboids.append(nc)
      else:
        voidCube = Cuboid(self.on, literals=(newMinX, self.maxX, newMinY, self.maxY, self.minZ, newMaxZ))
      if 'rtf' not in overlapPoints:
        # add rtf corner cuboid
        nc = Cuboid(self.on, literals=(newMinX, self.maxX, newMinY, self.maxY, newMinZ, self.maxZ))
        newCuboids.append(nc)
      else:
        voidCube = Cuboid(self.on, literals=(newMinX, self.maxX, newMinY, self.maxY, newMinZ, self.maxZ))
      
#     if any([nC.overlappedBy(voidCube) for nC in newCuboids]) or sum([nC.cellCount for nC in newCuboids]) + voidCube.cellCount != self.cellCount:
#       print('error: incorrect eighths')
#     if any([nC.overlappedBy(overlapper) for nC in newCuboids]):
#       print('error: eighths incorrectly positioned')
#     if not all([nC.whollyWithin(self) for nC in newCuboids]):
#       print('error: eighths overflowed original')
#     if not voidCube.whollyWithin(self) or not voidCube.whollyWithin(overlapper):
#       print('error: eighths void cube wrong')
      return newCuboids, voidCube.cellCount
    
    if len(overlapPoints) == 0:
      # overlap has no corners in, like a slice through another cube
      # find what axis slice is aligned on
      if self.minX <= overlapper.minX <= overlapper.maxX <= self.maxX:
        sliceAxis = 'X'
      elif self.minY <= overlapper.minY <= overlapper.maxY <= self.maxY:
        sliceAxis = 'Y'
      elif self.minZ <= overlapper.minZ <= overlapper.maxZ <= self.maxZ:
        sliceAxis = 'Z'

      # create two sides of slice
      if sliceAxis == 'X':
        s1 = Cuboid(self.on, literals=(self.minX, overlapper.minX-1, self.minY, self.maxY, self.minZ, self.maxZ))
        s2 = Cuboid(self.on, literals=(overlapper.maxX+1, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ))
      elif sliceAxis == 'Y':
        s1 = Cuboid(self.on, literals=(self.minX, self.maxX, self.minY, overlapper.minY-1, self.minZ, self.maxZ))
        s2 = Cuboid(self.on, literals=(self.minX, self.maxX, overlapper.maxY+1, self.maxY, self.minZ, self.maxZ))
      elif sliceAxis == 'Z':
        s1 = Cuboid(self.on, literals=(self.minX, self.maxX, self.minY, self.maxY, self.minZ, overlapper.minZ-1))
        s2 = Cuboid(self.on, literals=(self.minX, self.maxX, self.minY, self.maxY, overlapper.maxZ+1, self.maxZ))
      newCuboids.append(s1)
      newCuboids.append(s2)
      
      if sliceAxis == 'X':
        lowY = self.minY < overlapper.minY
        highY = self.maxY > overlapper.maxY
        lowZ = self.minZ < overlapper.minZ
        highZ = self.maxZ > overlapper.maxZ
        c1 = lowY and highZ
        c2 = highY and highZ
        c3 = lowY and lowZ
        c4 = highY and lowZ
        
        minZ = overlapper.minZ if lowZ else self.minZ
        maxZ = overlapper.maxZ if highZ else self.maxZ
        minY = overlapper.minY if lowY else self.minY
        maxY = overlapper.maxY if highY else self.maxY
        
        vMinX = overlapper.minX
        vMaxX = overlapper.maxX
        vMinY = minY
        vMaxY = maxY
        vMinZ = minZ
        vMaxZ = maxZ
        
        if lowY:
          lowYCuboid = Cuboid(self.on, literals=(overlapper.minX, overlapper.maxX, self.minY, overlapper.minY-1, minZ, maxZ))
          newCuboids.append(lowYCuboid)
        if highY:
          highYCuboid = Cuboid(self.on, literals=(overlapper.minX, overlapper.maxX, overlapper.maxY+1, self.maxY, minZ, maxZ))
          newCuboids.append(highYCuboid)
        if lowZ:
          lowZCuboid = Cuboid(self.on, literals=(overlapper.minX, overlapper.maxX, minY, maxY, self.minZ, overlapper.minZ-1))
          newCuboids.append(lowZCuboid)
        if highZ:
          highZCuboid = Cuboid(self.on, literals=(overlapper.minX, overlapper.maxX, minY, maxY, overlapper.maxZ+1, self.maxZ))
          newCuboids.append(highZCuboid)
        if c1:
          c1Cuboid = Cuboid(self.on, literals=(overlapper.minX, overlapper.maxX, self.minY, overlapper.minY-1, overlapper.maxZ+1, self.maxZ))
          newCuboids.append(c1Cuboid)
        if c2:
          c2Cuboid = Cuboid(self.on, literals=(overlapper.minX, overlapper.maxX, overlapper.maxY+1, self.maxY, overlapper.maxZ+1, self.maxZ))
          newCuboids.append(c2Cuboid)
        if c3:
          c3Cuboid = Cuboid(self.on, literals=(overlapper.minX, overlapper.maxX, self.minY, overlapper.minY-1, self.minZ, overlapper.minZ-1))
          newCuboids.append(c3Cuboid)
        if c4:
          c4Cuboid = Cuboid(self.on, literals=(overlapper.minX, overlapper.maxX, overlapper.maxY+1, self.maxY, self.minZ, overlapper.minZ-1))
          newCuboids.append(c4Cuboid)
      
      elif sliceAxis == 'Y':
        lowX = self.minX < overlapper.minX
        highX = self.maxX > overlapper.maxX
        lowZ = self.minZ < overlapper.minZ
        highZ = self.maxZ > overlapper.maxZ
        c1 = lowX and highZ
        c2 = highX and highZ
        c3 = lowX and lowZ
        c4 = highX and lowZ
        
        minX = overlapper.minX if lowX else self.minX
        maxX = overlapper.maxX if highX else self.maxX
        minZ = overlapper.minZ if lowZ else self.minZ
        maxZ = overlapper.maxZ if highZ else self.maxZ
        
        vMinX = minX
        vMaxX = maxX
        vMinY = overlapper.minY
        vMaxY = overlapper.maxY
        vMinZ = minZ
        vMaxZ = maxZ
        
        if lowX:
          lowXCuboid = Cuboid(self.on, literals=(self.minX, overlapper.minX-1, overlapper.minY, overlapper.maxY, minZ, maxZ))
          newCuboids.append(lowXCuboid)
        if highX:
          highXCuboid = Cuboid(self.on, literals=(overlapper.maxX+1, self.maxX, overlapper.minY, overlapper.maxY, minZ, maxZ))
          newCuboids.append(highXCuboid)
        if lowZ:
          lowZCuboid = Cuboid(self.on, literals=(minX, maxX, overlapper.minY, overlapper.maxY, self.minZ, overlapper.minZ-1))
          newCuboids.append(lowZCuboid)
        if highZ:
          highZCuboid = Cuboid(self.on, literals=(minX, maxX, overlapper.minY, overlapper.maxY, overlapper.maxZ+1, self.maxZ))
          newCuboids.append(highZCuboid)
        if c1:
          c1Cuboid = Cuboid(self.on, literals=(self.minX, overlapper.minX-1, overlapper.minY, overlapper.maxY, overlapper.maxZ+1, self.maxZ))
          newCuboids.append(c1Cuboid)
        if c2:
          c2Cuboid = Cuboid(self.on, literals=(overlapper.maxX+1, self.maxX, overlapper.minY, overlapper.maxY, overlapper.maxZ+1, self.maxZ))
          newCuboids.append(c2Cuboid)
        if c3:
          c3Cuboid = Cuboid(self.on, literals=(self.minX, overlapper.minX-1, overlapper.minY, overlapper.maxY, self.minZ, overlapper.minZ-1))
          newCuboids.append(c3Cuboid)
        if c4:
          c4Cuboid = Cuboid(self.on, literals=(overlapper.maxX+1, self.maxX, overlapper.minY, overlapper.maxY, self.minZ, overlapper.minZ-1))
          newCuboids.append(c4Cuboid)
        
      
      elif sliceAxis == 'Z':
        lowX = self.minX < overlapper.minX
        highX = self.maxX > overlapper.maxX
        lowY = self.minY < overlapper.minY
        highY = self.maxY > overlapper.maxY
        c1 = lowX and highY
        c2 = highX and highY
        c3 = lowX and lowY
        c4 = highX and lowY
        
        minX = overlapper.minX if lowX else self.minX
        maxX = overlapper.maxX if highX else self.maxX
        minY = overlapper.minY if lowY else self.minY
        maxY = overlapper.maxY if highY else self.maxY
        
        vMinX = minX
        vMaxX = maxX
        vMinY = minY
        vMaxY = maxY
        vMinZ = overlapper.minZ
        vMaxZ = overlapper.maxZ
        
        if lowX:
          lowXCuboid = Cuboid(self.on, literals=(self.minX, overlapper.minX-1, minY, maxY, overlapper.minZ, overlapper.maxZ))
          newCuboids.append(lowXCuboid)
        if highX:
          highXCuboid = Cuboid(self.on, literals=(overlapper.maxX+1, self.maxX, minY, maxY, overlapper.minZ, overlapper.maxZ))
          newCuboids.append(highXCuboid)
        if lowY:
          lowYCuboid = Cuboid(self.on, literals=(minX, maxX, self.minY, overlapper.minY-1, overlapper.minZ, overlapper.maxZ))
          newCuboids.append(lowYCuboid)
        if highY:
          highYCuboid = Cuboid(self.on, literals=(minX, maxX, overlapper.maxY+1, self.maxY, overlapper.minZ, overlapper.maxZ))
          newCuboids.append(highYCuboid)
        if c1:
          c1Cuboid = Cuboid(self.on, literals=(self.minX, overlapper.minX-1, overlapper.maxY+1, self.maxY, overlapper.minZ, overlapper.maxZ))
          newCuboids.append(c1Cuboid)
        if c2:
          c2Cuboid = Cuboid(self.on, literals=(overlapper.maxX+1, self.maxX, overlapper.maxY+1, self.maxY, overlapper.minZ, overlapper.maxZ))
          newCuboids.append(c2Cuboid)
        if c3:
          c3Cuboid = Cuboid(self.on, literals=(self.minX, overlapper.minX-1, self.minY, overlapper.minY-1, overlapper.minZ, overlapper.maxZ))
          newCuboids.append(c3Cuboid)
        if c4:
          c4Cuboid = Cuboid(self.on, literals=(overlapper.maxX+1, self.maxX, self.minY, overlapper.minY-1, overlapper.minZ, overlapper.maxZ))
          newCuboids.append(c4Cuboid)
      
      voidCube = Cuboid(self.on, literals=(vMinX, vMaxX, vMinY, vMaxY, vMinZ, vMaxZ))
#     if any([nC.overlappedBy(voidCube) for nC in newCuboids]) or sum([nC.cellCount for nC in newCuboids]) + voidCube.cellCount != self.cellCount:
#       print('error: incorrect slices')
#     if any([nC.overlappedBy(overlapper) for nC in newCuboids]):
#       print('error: slices incorrectly positioned')
#     if not all([nC.whollyWithin(self) for nC in newCuboids]):
#       print('error: slices overflowed original')
#     if not voidCube.whollyWithin(self) or not voidCube.whollyWithin(overlapper):
#       print('error: slice void cube wrong')
      return newCuboids, voidCube.cellCount
      
  def findIntersectionBoundaries(self, overlapper, overlapPointName):
    corners = {
      'lbk': (overlapper.maxX+1, overlapper.maxX, overlapper.maxY+1, overlapper.maxY, overlapper.maxZ+1, overlapper.maxZ),
      'lbf': (overlapper.maxX+1, overlapper.maxX, overlapper.maxY+1, overlapper.maxY, overlapper.minZ, overlapper.minZ-1),
      'ltk': (overlapper.maxX+1, overlapper.maxX, overlapper.minY, overlapper.minY-1, overlapper.maxZ+1, overlapper.maxZ),
      'ltf': (overlapper.maxX+1, overlapper.maxX, overlapper.minY, overlapper.minY-1, overlapper.minZ, overlapper.minZ-1),
      'rbk': (overlapper.minX, overlapper.minX-1, overlapper.maxY+1, overlapper.maxY, overlapper.maxZ+1, overlapper.maxZ),
      'rbf': (overlapper.minX, overlapper.minX-1, overlapper.maxY+1, overlapper.maxY, overlapper.minZ, overlapper.minZ-1),
      'rtk': (overlapper.minX, overlapper.minX-1, overlapper.minY, overlapper.minY-1, overlapper.maxZ+1, overlapper.maxZ),
      'rtf': (overlapper.minX, overlapper.minX-1, overlapper.minY, overlapper.minY-1, overlapper.minZ, overlapper.minZ-1),
    }
    return corners[overlapPointName]
  
  def edgeCutCubeResults(self, overlapper, overlapPointNames):
    edges = {
      'lb': (
        (overlapper.maxX+1, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ),
        (self.minX, overlapper.maxX, overlapper.maxY+1, self.maxY, self.minZ, self.maxZ),
        (self.minX, overlapper.maxX, self.minY, overlapper.maxY, self.minZ, self.maxZ)
      ),
      'lk': (
        (overlapper.maxX+1, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ),
        (self.minX, overlapper.maxX, self.minY, self.maxY, overlapper.maxZ+1, self.maxZ),
        (self.minX, overlapper.maxX, self.minY, self.maxY, self.minZ, overlapper.maxZ)
      ),
      'bk': (
        (self.minX, self.maxX, overlapper.maxY+1, self.maxY, self.minZ, self.maxZ),
        (self.minX, self.maxX, self.minY, overlapper.maxY, overlapper.maxZ+1, self.maxZ),
        (self.minX, self.maxX, self.minY, overlapper.maxY, self.minZ, overlapper.maxZ)
      ),
      'lf': (
        (overlapper.maxX+1, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ),
        (self.minX, overlapper.maxX, self.minY, self.maxY, self.minZ, overlapper.minZ-1),
        (self.minX, overlapper.maxX, self.minY, self.maxY, overlapper.minZ, self.maxZ)
      ),
      'bf': (
        (self.minX, self.maxX, self.minY, self.maxY, self.minZ, overlapper.minZ-1),
        (self.minX, self.maxX, overlapper.maxY+1, self.maxY, overlapper.minZ, self.maxZ),
        (self.minX, self.maxX, self.minY, overlapper.maxY, overlapper.minZ, self.maxZ)
      ),
      'lt': (
        (overlapper.maxX+1, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ),
        (self.minX, overlapper.maxX, self.minY, overlapper.minY-1, self.minZ, self.maxZ),
        (self.minX, overlapper.maxX, overlapper.minY, self.maxY, self.minZ, self.maxZ)
      ),
      'tk': (
        (self.minX, self.maxX, self.minY, overlapper.minY-1, self.minZ, self.maxZ),
        (self.minX, self.maxX, overlapper.minY, self.maxY, overlapper.maxZ+1, self.maxZ),
        (self.minX, self.maxX, overlapper.minY, self.maxY, self.minZ, overlapper.maxZ)
      ),
      'tf': (
        (self.minX, self.maxX, self.minY, overlapper.minY-1, self.minZ, self.maxZ),
        (self.minX, self.maxX, overlapper.minY, self.maxY, self.minZ, overlapper.minZ-1),
        (self.minX, self.maxX, overlapper.minY, self.maxY, overlapper.minZ, self.maxZ)
      ),
      'rb': (
        (self.minX, overlapper.minX-1, self.minY, self.maxY, self.minZ, self.maxZ),
        (overlapper.minX, self.maxX, overlapper.maxY+1, self.maxY, self.minZ, self.maxZ),
        (overlapper.minX, self.maxX, self.minY, overlapper.maxY, self.minZ, self.maxZ)
      ),
      'rk': (
        (self.minX, overlapper.minX-1, self.minY, self.maxY, self.minZ, self.maxZ),
        (overlapper.minX, self.maxX, self.minY, self.maxY, overlapper.maxZ+1, self.maxZ),
        (overlapper.minX, self.maxX, self.minY, self.maxY, self.minZ, overlapper.maxZ)
      ),
      'rf': (
        (self.minX, overlapper.minX-1, self.minY, self.maxY, self.minZ, self.maxZ),
        (overlapper.minX, self.maxX, self.minY, self.maxY, self.minZ, overlapper.minZ-1),
        (overlapper.minX, self.maxX, self.minY, self.maxY, overlapper.minZ, self.maxZ)
      ),
      'rt': (
        (self.minX, overlapper.minX-1, self.minY, self.maxY, self.minZ, self.maxZ),
        (overlapper.minX, self.maxX, self.minY, overlapper.minY-1, self.minZ, self.maxZ),
        (overlapper.minX, self.maxX, overlapper.minY, self.maxY, self.minZ, self.maxZ)
      ),
    }
    c1, c2 = overlapPointNames
    edgeName = ''.join([x for x in c1 if x in c2])
    return edges[edgeName]
    
  def findCutCorners(self, overlapper):
    corners = {
      'lbk': (self.minX, self.minY, self.minZ),
      'lbf': (self.minX, self.minY, self.maxZ),
      'ltk': (self.minX, self.maxY, self.minZ),
      'ltf': (self.minX, self.maxY, self.maxZ),
      'rbk': (self.maxX, self.minY, self.minZ),
      'rbf': (self.maxX, self.minY, self.maxZ),
      'rtk': (self.maxX, self.maxY, self.minZ),
      'rtf': (self.maxX, self.maxY, self.maxZ),
    }
    for code, coords in corners.items():
      if overlapper.cellIn(coords):
        corners[code] = True
      else:
        corners[code] = False
        
    return corners
  
  def isSlicedBy(self, overlapper):
    x1 = self.minX <= overlapper.minX <= self.maxX
    x2 = self.minX <= overlapper.maxX <= self.maxX
    xM = x1 and x2
    x3 = overlapper.minX <= self.minX <= self.maxX <= overlapper.maxX
    
    y1 = self.minY <= overlapper.minY <= self.maxY
    y2 = self.minY <= overlapper.maxY <= self.maxY
    yM = y1 and y2
    y3 = overlapper.minY <= self.minY <= self.maxY <= overlapper.maxY
    
    z1 = self.minZ <= overlapper.minZ <= self.maxZ
    z2 = self.minZ <= overlapper.maxZ <= self.maxZ
    zM = z1 and z2
    z3 = overlapper.minZ <= self.minZ <= self.maxZ <= overlapper.maxZ
    
    xslice = xM and ((y1 or y2 or y3) and (z1 or z2 or z3))
    yslice = yM and ((x1 or x2 or x3) and (z1 or z2 or z3))
    zslice = zM and ((x1 or x2 or x3) and (y1 or y2 or y3))
    
    return xslice or yslice or zslice
  
  def overlappedBy(self, other):
    return len([corner for corner, cut in self.findCutCorners(other).items() if cut == True]) > 0 or self.isSlicedBy(other)
    
  def findCellCount(self):
    if self.on:
      x = self.maxX+1-self.minX
      y = self.maxY+1-self.minY
      z = self.maxZ+1-self.minZ
      return x*y*z
    return 0

fileName = 'data.txt'
instructions = [x.strip().split(' ') for x in open(fileName).readlines()]
totalCount = 0
cuboids = []
for onOff, coords in instructions:
  oldTotal = totalCount
  totalVoids = 0
  cube = Cuboid(onOff == 'on', coords)
# print(onOff, coords)
  
  newCuboids = []
  for o in cuboids:
    if o.overlappedBy(cube):
      splitCuboids, voidSum = o.splitCuboid(cube)
      totalVoids += voidSum
      if splitCuboids:
        newCuboids += splitCuboids
    else:
      newCuboids.append(o)
  
  if cube.on:
    newCuboids.append(cube)
  
  cuboids = newCuboids

  totalCount = sum(c.cellCount for c in cuboids if c.on)
  
# if totalCount != oldTotal + cube.cellCount - totalVoids:
#   print('error: mystery cells')
  
print(f'All {len(cuboids)} cubes: {totalCount} cells')