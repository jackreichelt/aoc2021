#!/usr/bin/env python3

rows = [r.strip() for r in open('data.txt').readlines()]

MAXY = len(rows)
MAXX = len(rows[0])

def printCucumbers(rightHerd, downHerd):
  for y in range(MAXY):
    for x in range(MAXX):
      if (x,y) in rightHerd:
        print('>', end='')
      elif (x,y) in downHerd:
        print('v', end='')
      else:
        print('.', end='')
    print()
  print()

rightCucumbers = set()
downCucumbers = set()

for y, row in enumerate(rows):
  for x, c in enumerate(row):
    if c == '>':
      rightCucumbers.add((x,y))
    elif c == 'v':
      downCucumbers.add((x,y))

static = False
steps = 0
while not static:
  steps += 1
  static = True
  newRightCucumbers = set()
  newDownCucumbers = set()
  
  for c in rightCucumbers:
    new = (c[0]+1, c[1])
    if new[0] >= MAXX:
      new = (0, c[1])
    if new not in rightCucumbers and new not in downCucumbers:
      newRightCucumbers.add(new)
      static = False
    else:
      newRightCucumbers.add(c)
  rightCucumbers = newRightCucumbers
  
  for c in downCucumbers:
    new = (c[0], c[1]+1)
    if new[1] >= MAXY:
      new = (c[0], 0)
    if new not in rightCucumbers and new not in downCucumbers:
      newDownCucumbers.add(new)
      static = False
    else:
      newDownCucumbers.add(c)
  downCucumbers = newDownCucumbers
  
print(f'Took {steps} steps until safe to land.')