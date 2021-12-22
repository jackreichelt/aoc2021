#!/usr/bin/env python3
from itertools import combinations, permutations
from math import sqrt

class Scanner():
  def __init__(self, bId, beacons):
    self.id = bId
    self.x = 0
    self.y = 0
    self.beacons = {i: beacon for i, beacon in enumerate(beacons)}
    self.beaconDistancePairs = Scanner.beaconDistances(self.beacons)
    
    self.anchored = False
    self.relativePosition = (0,0,0)
    
    if self.id == 0:
      self.anchored = True
    
  def pointDistance(b1, b2):
    x1, y1, z1 = b1
    x2, y2, z2 = b2
    
    return sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
  
  def beaconDistances(beacons):
    beaconDistances = {}
    beaconPairs = combinations(beacons.items(), 2)
    
    for b1, b2 in beaconPairs:
      id1, coords1 = b1
      id2, coords2 = b2
      
      beaconDistances[Scanner.pointDistance(coords1, coords2)] = (id1, id2)
      
    return beaconDistances
  
  def findRotationsOfPoint(point):
    x,y,z = point
    
    rotations = [
      (x,y,z),
      (x,z,-y),
      (x,-y,-z),
      (x,-z,y),
      (y,x,-z),
      (y,z,x),
      (y,-x,z),
      (y,-z,-x),
      (z,x,y),
      (z,y,-x),
      (z,-x,-y),
      (z,-y,x),
      (-x,y,-z),
      (-x,z,y),
      (-x,-y,z),
      (-x,-z,-y),
      (-y,x,z),
      (-y,z,-x),
      (-y,-x,-z),
      (-y,-z,x),
      (-z,x,-y),
      (-z,y,x),
      (-z,-x,y),
      (-z,-y,-x),
    ]
    return rotations
  
  def findUnitRotation(i):
    x,y,z = ('x','y','z')
    
    rotations = [
      (x,y,z),
      (x,z,'-'+y),
      (x,'-'+y,'-'+z),
      (x,'-'+z,y),
      (y,x,'-'+z),
      (y,z,x),
      (y,'-'+x,z),
      (y,'-'+z,'-'+x),
      (z,x,y),
      (z,y,'-'+x),
      (z,'-'+x,'-'+y),
      (z,'-'+y,x),
      ('-'+x,y,'-'+z),
      ('-'+x,z,y),
      ('-'+x,'-'+y,z),
      ('-'+x,'-'+z,'-'+y),
      ('-'+y,x,z),
      ('-'+y,z,'-'+x),
      ('-'+y,'-'+x,'-'+z),
      ('-'+y,'-'+z,x),
      ('-'+z,x,'-'+y),
      ('-'+z,y,x),
      ('-'+z,'-'+x,y),
      ('-'+z,'-'+y,'-'+x),
    ]
    return rotations[i]
  
  def rotationLambdas(index):
    lambdas = [
      lambda x,y,z: (x,y,z),
      lambda x,y,z: (x,z,-y),
      lambda x,y,z: (x,-y,-z),
      lambda x,y,z: (x,-z,y),
      lambda x,y,z: (y,x,-z),
      lambda x,y,z: (y,z,x),
      lambda x,y,z: (y,-x,z),
      lambda x,y,z: (y,-z,-x),
      lambda x,y,z: (z,x,y),
      lambda x,y,z: (z,y,-x),
      lambda x,y,z: (z,-x,-y),
      lambda x,y,z: (z,-y,x),
      lambda x,y,z: (-x,y,-z),
      lambda x,y,z: (-x,z,y),
      lambda x,y,z: (-x,-y,z),
      lambda x,y,z: (-x,-z,-y),
      lambda x,y,z: (-y,x,z),
      lambda x,y,z: (-y,z,-x),
      lambda x,y,z: (-y,-x,-z),
      lambda x,y,z: (-y,-z,x),
      lambda x,y,z: (-z,x,-y),
      lambda x,y,z: (-z,y,x),
      lambda x,y,z: (-z,-x,y),
      lambda x,y,z: (-z,-y,-x),
    ]
    return lambdas[index]
  
  def transformPoints(self, rotationLambda, translation):
    newBeacons = {}
    for bid, coords in self.beacons.items():
      x,y,z = coords
      newCoords = rotationLambda(x,y,z)
      newBeacons[bid] = (newCoords[0]+translation[0], newCoords[1]+translation[1], newCoords[2]+translation[2])
    self.beacons = newBeacons
    self.beaconDistancePairs = Scanner.beaconDistances(self.beacons)
    self.anchored = True
    return True
  
  def findBeaconOverlaps(self, other):
    if not self.anchored or other.anchored:
      return
    s1 = self
    s2 = other
    s1BeaconSet = set(s1.beaconDistancePairs)
    s2BeaconSet = set(s2.beaconDistancePairs)
    
    overlap = s1BeaconSet.intersection(s2BeaconSet)
    overlapBeacons = set()
    
    for dist in overlap:
      b1, b2 = s1.beaconDistancePairs[dist]
      overlapBeacons.add(b1)
      overlapBeacons.add(b2)
      
    if len(overlapBeacons) >= 12:
      tentativeRelsX = []
      tentativeRelsY = []
      tentativeRelsZ = []
      
      for dist in overlap:
        s1BId1, s1BId2 = s1.beaconDistancePairs[dist]
        s2BId1, s2BId2 = s2.beaconDistancePairs[dist]
        
        s1B1x, s1B1y, s1B1z = s1.beacons[s1BId1]
        s1B2x, s1B2y, s1B2z = s1.beacons[s1BId2]
        
        s2B1Rotations = Scanner.findRotationsOfPoint(s2.beacons[s2BId1])
        s2B2Rotations = Scanner.findRotationsOfPoint(s2.beacons[s2BId2])
        
        for i, s2Point1 in enumerate(s2B1Rotations):
          s2Point2 = s2B2Rotations[i]
          
          s2B1x, s2B1y, s2B1z = s2Point1
          s2B2x, s2B2y, s2B2z = s2Point2
          
          potentialRelX1 = s1B1x - s2B1x
          potentialRelY1 = s1B1y - s2B1y
          potentialRelZ1 = s1B1z - s2B1z
          potentialRelX2 = s1B2x - s2B2x
          potentialRelY2 = s1B2y - s2B2y
          potentialRelZ2 = s1B2z - s2B2z
          
          if potentialRelX1 == potentialRelX2 and potentialRelY1 == potentialRelY2 and potentialRelZ1 == potentialRelZ2:
            if potentialRelX1 in tentativeRelsX and potentialRelY1 in tentativeRelsY and potentialRelZ1 in tentativeRelsZ:
              print(f'Relation found between Scanner {s1.id} and Scanner {s2.id}: {",".join(Scanner.findUnitRotation(i))}, ({potentialRelX1}, {potentialRelY1}, {potentialRelZ1})')
              s2.relativePosition = (potentialRelX1, potentialRelY1, potentialRelZ1)
              s2.transformPoints(Scanner.rotationLambdas(i), (potentialRelX1, potentialRelY1, potentialRelZ1))
              return True
            tentativeRelsX.append(potentialRelX1)
            tentativeRelsY.append(potentialRelY1)
            tentativeRelsZ.append(potentialRelZ1)
                        
      print(f'No relation found between Scanner {s1.id} and Scanner {s2.id}!!!')
      return False
  
beaconLists = [x.split('\n') for x in open('data.txt').read().split('\n\n')]
scanners = []
for beaconList in beaconLists:
  bId = int(beaconList[0].split(' ')[2])
  beacons = []
  for beacon in beaconList[1:]:
    x, y, z = beacon.split(',')
    beacons.append((int(x), int(y), int(z)))
    
  scanners.append(Scanner(bId, beacons))
  
while any([not s.anchored for s in scanners]):
  for s1, s2 in permutations(scanners, 2):
    s1.findBeaconOverlaps(s2)

foundBeacons = set().union(*[s.beacons.values() for s in scanners])

print('Number of beacons:', len(foundBeacons)) # Part 1: 396

print('Max distance:', max([sum([abs(s1.relativePosition[0]-s2.relativePosition[0]), abs(s1.relativePosition[1]-s2.relativePosition[1]), abs(s1.relativePosition[2]-s2.relativePosition[2])]) for s1, s2 in permutations(scanners, 2)])) # Part 2: 11828