#!/usr/bin/env python3

data = dotsString, foldsString = open('data.txt').read().split("\n\n")

dots = [[int(x) for x in dot.strip().split(',')] for dot in dotsString.split('\n')]

def printDots():
  maxX = max(x for x,y in dots)+1
  maxY = max(y for x,y in dots)+1
  
  for y in range(maxY):
    for x in range(maxX):
      if [x,y] in dots:
        print('#', end='')
      else:
        print('.', end='')
    print()
  print()
  
#printDots()
for fold in foldsString.split('\n'):
  direction = fold.strip().split('=')[0][-1]
  foldValue = int(fold.strip().split('=')[1])
  
  dirIndex = 0 if direction == 'x' else 1
  
  newDots = []
  for dot in dots:		
    if dot[dirIndex] > foldValue:
      if direction == 'x':
        newDot = [foldValue - (dot[0]-foldValue), dot[1]]
        
      else:
        newDot = [dot[0], foldValue - (dot[1]-foldValue)]
      if newDot not in newDots:
        newDots.append(newDot)
    else:
      newDots.append(dot)
    dots = newDots
  
  print(len({f'{x},{y}' for x, y in dots})) # Part 1: 669
printDots()
