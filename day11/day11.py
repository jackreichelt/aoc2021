#!/usr/bin/env python3

data = [x.strip() for x in open('data.txt').readlines()]

class Octopus():
  def __init__(self, x, y, energy):
    self.x = x
    self.y = y
    self.adjacents = []
    self.energy = energy
    self.flashed = False
    self.flashes = 0
    
  def addAdjacents(self, allOctopuses):
    xRange = (self.x-1, self.x, self.x+1)
    yRange = (self.y-1, self.y, self.y+1)
    self.adjacents = [octo for octo in allOctopuses if octo.x in xRange and octo.y in yRange and not (octo.x == self.x and octo.y == self.y)]
    
  def increase(self):
    self.energy += 1

  def flash(self):
    if self.energy > 9 and not self.flashed:
      self.flashed = True
      self.flashes += 1
      for adj in self.adjacents:
        adj.increase()
      return True
    return False
  
  def reset(self):
    if self.flashed:
      self.energy = 0
      self.flashed = False
      
def printOctos(allOctos):
  for y in range(10):
    for x in range(10):
      print(allOctos[y*10+x].energy, end='')
    print()
  print()

allOctos = []

for y, row in enumerate(data):
  for x, energy in enumerate(row):
    allOctos.append(Octopus(x, y, int(energy)))

for octo in allOctos:
  octo.addAdjacents(allOctos)

for i in range(1000):
  for octo in allOctos:
    octo.increase()
  flashes = [octo.flash() for octo in allOctos]
  while any(flashes):
    flashes = [octo.flash() for octo in allOctos]
    
  if all([octo.flashed for octo in allOctos]):
    print('All octopuses flashed on step:', i+1)
    break
  for octo in allOctos:
    octo.reset()

print('Total Flashes:', sum(octo.flashes for octo in allOctos))