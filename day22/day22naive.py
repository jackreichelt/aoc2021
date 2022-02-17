#!/usr/bin/env python3

cells = set()

instructions = [x.strip().split(' ') for x in open('data.txt').readlines()]

for onOff, coords in instructions:
  print(onOff, coords)
  x,y,z = coords.split(',')
  minX, maxX = (int(num) for num in x[2:].split('..'))
  minY, maxY = (int(num) for num in y[2:].split('..'))
  minZ, maxZ = (int(num) for num in z[2:].split('..'))
  
  if onOff == 'on':
    for x in range(minX, maxX+1):
      for y in range(minY, maxY+1):
        for z in range(minZ, maxZ+1):
          cells.add((x,y,z))
  else:
    for x in range(minX, maxX+1):
      for y in range(minY, maxY+1):
        for z in range(minZ, maxZ+1):
          cells.discard((x,y,z))
  
  print(f'{len(cells)} cells')
          