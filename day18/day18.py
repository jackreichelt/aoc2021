#!/usr/bin/env python3
from itertools import permutations
from math import floor, ceil

class SnailfishNumber():
  
  def findParts(numString):
    bracketPairs = numString.count('[')
    middleIndex = len(numString)//2
    left, right = numString[1:middleIndex].rstrip(','), numString[middleIndex:-1].lstrip(',')
    
    while left.count('[') != left.count(']') or right.count('[') != right.count(']'):
      if left.count('[') > left.count(']'):
        middleIndex += 1
      else:
        middleIndex -= 1
      left, right = numString[1:middleIndex].rstrip(','), numString[middleIndex:-1].lstrip(',')
      
    if len(right) != 0:
      return left, right
    
    middleIndex = len(numString)//2
    left, right = numString[1:middleIndex].rstrip(','), numString[middleIndex:-1].lstrip(',')
    
    while left.count('[') != left.count(']') or right.count('[') != right.count(']'):
      if right.count('[') > right.count(']'):
        middleIndex += 1
      else:
        middleIndex -= 1
      left, right = numString[1:middleIndex].rstrip(','), numString[middleIndex:-1].lstrip(',')
      
    return left, right
  
  def __init__(self, numString=None, left=None, right=None, parent=None):
    self.parent = parent
    self.leftLiteral = False
    self.rightLiteral = False
    if numString:
      leftStr, rightStr = SnailfishNumber.findParts(numString)
      if '[' in leftStr:
        self.left = SnailfishNumber(leftStr, parent=self)
      else:
        self.left = int(leftStr)
        self.leftLiteral = True
      if '[' in rightStr:
        self.right = SnailfishNumber(rightStr, parent=self)
      else:
        self.right = int(rightStr)
        self.rightLiteral = True
    else:
      self.left = left
      self.right = right
      left.parent = self
      right.parent = self
      
  def __str__(self):
    return f'[{self.left},{self.right}]'
  
  def __add__(self, o):
    newSnailfishNumber = SnailfishNumber(left=self, right=o, parent=self)
    
    while newSnailfishNumber.needsAdjustment():
      if newSnailfishNumber.needsExploding():
        newSnailfishNumber.explode(newSnailfishNumber.findExplosionPath())
      elif newSnailfishNumber.needsSplit():
        newSnailfishNumber.split(newSnailfishNumber.findSplitPath())
        
    return newSnailfishNumber
  
  def __radd__(self, other):
    if other == 0:
      return self
    else:
      return self.__add__(other)
    
  def toString(self):
    return self.__str__()

  def findNodeFromPath(self, path):
    target = self
    for side in path:
      if side == 'l':
        target = target.left
      else:
        target = target.right
    return target
  
  def mag(self):
    lMag = 3*self.left if self.leftLiteral else 3*self.left.mag()
    rMag = 2*self.right if self.rightLiteral else 2*self.right.mag()
    
    return lMag + rMag
  
  def needsAdjustment(self):
    return self.needsSplit() or self.needsExploding()
  
  def needsSplit(self):
    if self.leftLiteral:
      lSplit = self.left >= 10
    else:
      lSplit = self.left.needsSplit()
      
    if self.rightLiteral:
      rSplit = self.right >= 10
    else:
      rSplit = self.right.needsSplit()
      
    return lSplit or rSplit
  
  def findSplitPath(self, splitPath=''):
    if self.leftLiteral:
      if self.left >= 10:
        return splitPath+'l'
      else:
        lSplit = False
    else:
      lSplit = self.left.findSplitPath(splitPath+'l')
    if lSplit != False:
      return lSplit
      
    if self.rightLiteral:
      if self.right >= 10:
        return splitPath+'r'
      else:
        rSplit =  False
    else:
      rSplit = self.right.findSplitPath(splitPath+'r')
    if rSplit != False:
      return rSplit
    
    return False
    
  def split(self, path):
    if len(path) == 1:
      if path == 'l':
        self.left = SnailfishNumber(f'[{floor(self.left/2)},{ceil(self.left/2)}]', parent=self)
        self.leftLiteral = False
      else:
        self.right = SnailfishNumber(f'[{floor(self.right/2)},{ceil(self.right/2)}]', parent=self)
        self.rightLiteral = False
    else:
      side, nextPath = path[0], path[1:]
      if side == 'l':
        self.left.split(nextPath)
      else:
        self.right.split(nextPath)
  
  def needsExploding(self, currentDepth=0):
    if currentDepth >= 4:
      return True
    
    if self.leftLiteral:
      lExplode = False
    else:
      lExplode = self.left.needsExploding(currentDepth+1)
      
    if self.rightLiteral:
      rExplode = False
    else:
      rExplode = self.right.needsExploding(currentDepth+1)
      
    return lExplode or rExplode
  
  def findExplosionPath(self, explosionPath='', currentDepth=0):
    if currentDepth >= 4:
      if self.leftLiteral and self.rightLiteral:
        return explosionPath
      elif not self.leftLiteral:
        return self.left.findExplosionPath(explosionPath+'l', currentDepth+1)
      else:
        return self.right.findExplosionPath(explosionPath+'r', currentDepth+1)
    
    if self.leftLiteral:
      lExplode = False
    else:
      lExplode = self.left.findExplosionPath(explosionPath+'l', currentDepth+1)
      
    if self.rightLiteral:
      rExplode = False
    else:
      rExplode = self.right.findExplosionPath(explosionPath+'r', currentDepth+1)
      
    return lExplode or rExplode
    
  def explode(self, path):
    target = self.findNodeFromPath(path)
    
    leftVal = target.left
    rightVal = target.right
    
    if path[-1] == 'l':
      if target.parent.rightLiteral:
        target.parent.right += rightVal
      else:
        rTarget = target.parent.right
        while not rTarget.leftLiteral:
          rTarget = rTarget.left
        rTarget.left += rightVal
      
      if 'r' in path:
        lPath = path[:path.rfind('r')]
        lTarget = self.findNodeFromPath(lPath)
        if lTarget.leftLiteral:
          lTarget.left += leftVal
        else:
          lTarget = lTarget.left
          while not lTarget.rightLiteral:
            lTarget = lTarget.right
          lTarget.right += leftVal
    
    else:
      if target.parent.leftLiteral:
        target.parent.left += leftVal
      else:
        lTarget = target.parent.left
        while not lTarget.rightLiteral:
          lTarget = lTarget.left
        lTarget.right += leftVal
    
      if 'l' in path:
        rPath = path[:path.rfind('l')]
        rTarget = self.findNodeFromPath(rPath)
        if rTarget.rightLiteral:
          rTarget.right += rightVal
        else:
          rTarget = rTarget.right
          while not rTarget.leftLiteral:
            rTarget = rTarget.left
          rTarget.left += rightVal
    
    if path[-1] == 'l':
      target.parent.left = 0
      target.parent.leftLiteral = True
    else:
      target.parent.right = 0
      target.parent.rightLiteral = True
    
    
      
print('Beginning tests...')
print('Testing SnailfishNumber::__init__')
t1 = SnailfishNumber('[1,2]')
t2 = SnailfishNumber('[[1,2],3]')
t3 = SnailfishNumber('[9,[8,7]]')
t4 = SnailfishNumber('[[1,9],[8,5]]')
t5 = SnailfishNumber('[[[[1,2],[3,4]],[[5,6],[7,8]]],9]')
print('[1,2]', t1)
print('[[1,2],3]', t2)
print('[9,[8,7]]', t3)
print('[[1,9],[8,5]]', t4)
print('[[[[1,2],[3,4]],[[5,6],[7,8]]],9]', t5)
print()

print('Testing SnailfishNumber::__add__ and SnailfishNumber::__radd__')
addT1 = SnailfishNumber('[1,2]')
addT2 = SnailfishNumber('[[3,4],5]')
addR1 = addT1 + addT2
print('[[1,2],[[3,4],5]]', addR1)
add1 = SnailfishNumber('[1,1]')
add2 = SnailfishNumber('[2,2]')
add3 = SnailfishNumber('[3,3]')
add4 = SnailfishNumber('[4,4]')
addR2 = add1 + add2 + add3 + add4
print('[[[[1,1],[2,2]],[3,3]],[4,4]]', addR2)
sumR2 = sum([add1, add2, add3, add4])
print('[[[[1,1],[2,2]],[3,3]],[4,4]]', sumR2)
print()

print('Testing SnailfishNumber::needsSplit')
print('True', SnailfishNumber('[10,0]').needsSplit())
print('True', SnailfishNumber('[0,11]').needsSplit())
print('True', SnailfishNumber('[12,0]').needsSplit())
print('False', t5.needsSplit())
print('False', addR1.needsSplit())
print('True', SnailfishNumber('[[[[0,7],4],[15,[0,13]]],[1,1]]').needsSplit())
print()

print('Testing SnailfishNumber::findSplitPath')
print('l', SnailfishNumber('[10,0]').findSplitPath())
print('r', SnailfishNumber('[0,11]').findSplitPath())
print('l', SnailfishNumber('[12,0]').findSplitPath())
print('False', t5.findSplitPath())
print('False', addR1.findSplitPath())
print('lrl', SnailfishNumber('[[[[0,7],4],[15,[0,13]]],[1,1]]').findSplitPath())
print('lrrr', SnailfishNumber('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]').findSplitPath())
print()

print('Testing SnailfishNumber::split')
splitT1 = SnailfishNumber('[10,0]')
splitT2 = SnailfishNumber('[0,11]')
splitT3 = SnailfishNumber('[12,0]')
splitT1.split('l')
splitT2.split('r')
splitT3.split('l')
print('[[5,5],0]', splitT1)
print('[0,[5,6]]', splitT2)
print('[[6,6],0]', splitT3)
splitT4 = SnailfishNumber('[[[[0,7],4],[15,[0,13]]],[1,1]]')
splitT5 = SnailfishNumber('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]')
splitT4.split('lrl')
splitT5.split('lrrr')
print('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]', splitT4)
print('[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]', splitT5)
print()

print('Testing SnailfishNumber::needsExploding')
print('True', SnailfishNumber('[[[[[9,8],1],2],3],4]').needsExploding())
print('True', SnailfishNumber('[7,[6,[5,[4,[3,2]]]]]').needsExploding())
print('True', SnailfishNumber('[[6,[5,[4,[3,2]]]],1]').needsExploding())
print('True', SnailfishNumber('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]').needsExploding())
print('False', t5.needsExploding())
print('False', addR1.needsExploding())
print()

print('Testing SnailfishNumber::findExplosion')
print('llll', SnailfishNumber('[[[[[9,8],1],2],3],4]').findExplosionPath())
print('rrrr', SnailfishNumber('[7,[6,[5,[4,[3,2]]]]]').findExplosionPath())
print('lrrr', SnailfishNumber('[[6,[5,[4,[3,2]]]],1]').findExplosionPath())
print('lrrr', SnailfishNumber('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]').findExplosionPath())
print()

print('Testing SnailfishNumber::explode')
eT1 = SnailfishNumber('[[[[[9,8],1],2],3],4]')
eT1.explode(eT1.findExplosionPath())
print('[[[[0,9],2],3],4]', eT1)
eT2 = SnailfishNumber('[7,[6,[5,[4,[3,2]]]]]')
eT2.explode(eT2.findExplosionPath())
print('[7,[6,[5,[7,0]]]]', eT2)
eT3 = SnailfishNumber('[[6,[5,[4,[3,2]]]],1]')
eT3.explode(eT3.findExplosionPath())
print('[[6,[5,[7,0]]],3]', eT3)
eT4 = SnailfishNumber('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
eT4.explode(eT4.findExplosionPath())
print('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', eT4)
print()

print('Testing full sums')
fT0 = SnailfishNumber('[[[[4,3],4],4],[7,[[8,4],9]]]') + SnailfishNumber('[1,1]')
print('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]', fT0)
fT1 = [
  SnailfishNumber('[1,1]'),
  SnailfishNumber('[2,2]'),
  SnailfishNumber('[3,3]'),
  SnailfishNumber('[4,4]'),
  SnailfishNumber('[5,5]')
]
print('[[[[3,0],[5,3]],[4,4]],[5,5]]', sum(fT1))
fT2 = [
  SnailfishNumber('[1,1]'),
  SnailfishNumber('[2,2]'),
  SnailfishNumber('[3,3]'),
  SnailfishNumber('[4,4]'),
  SnailfishNumber('[5,5]'),
  SnailfishNumber('[6,6]')
]
print('[[[[5,0],[7,4]],[5,5]],[6,6]]', sum(fT2))
fT2 = [
  SnailfishNumber('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]'),
  SnailfishNumber('[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]'),
  SnailfishNumber('[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]'),
  SnailfishNumber('[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]'),
  SnailfishNumber('[7,[5,[[3,8],[1,4]]]]'),
  SnailfishNumber('[[2,[2,2]],[8,[8,1]]]'),
  SnailfishNumber('[2,9]'),
  SnailfishNumber('[1,[[[9,3],9],[[9,0],[0,7]]]]'),
  SnailfishNumber('[[[5,[7,4]],7],1]'),
  SnailfishNumber('[[[[4,2],2],6],[8,7]]')
]
print('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]', sum(fT2))
print()

print('Testing SnailfishNumber::mag')
print('29', SnailfishNumber('[9,1]').mag())
print('143', SnailfishNumber('[[1,2],[[3,4],5]]').mag())
print('1384', SnailfishNumber('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]').mag())
print('445', SnailfishNumber('[[[[1,1],[2,2]],[3,3]],[4,4]]').mag())
print('791', SnailfishNumber('[[[[3,0],[5,3]],[4,4]],[5,5]]').mag())
print('1137', SnailfishNumber('[[[[5,0],[7,4]],[5,5]],[6,6]]').mag())
print('3488', SnailfishNumber('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]').mag())
print()

homeworkTest = [SnailfishNumber(x.strip()) for x in open('test.txt').readlines()]
homeworkTestSum = sum(homeworkTest)
print('[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]', homeworkTestSum)
print('4140', homeworkTestSum.mag())
print()

homework = [SnailfishNumber(x.strip()) for x in open('data.txt').readlines()]
homeworkSum = sum(homework)
print('Homework answer:', homeworkSum)
print('Homework magnitude:', homeworkSum.mag())

bestNumber = None
bestMag = 0

for a,b in permutations([x.strip() for x in open('test.txt').readlines()], r=2):
  a = SnailfishNumber(a)
  b = SnailfishNumber(b)
  
  c = a + b
  cMag = c.mag()
  if cMag > bestMag:
    bestMag = cMag
    bestNumber = c

print('[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]', bestNumber)
print('3993', bestMag)

for a,b in permutations([x.strip() for x in open('data.txt').readlines()], r=2):
  a = SnailfishNumber(a)
  b = SnailfishNumber(b)
  
  c = a + b
  cMag = c.mag()
  if cMag > bestMag:
    bestMag = cMag
    bestNumber = c
    
print('Best pair:', bestNumber)
print('Best magnitude:', bestMag)