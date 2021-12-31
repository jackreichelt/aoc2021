#!/usr/bin/env python3
from heapq import heappush, heappop

LAYOUT1 = """#############
#...........#
###D#D#C#B###
  #B#A#A#C#
  #########
"""
  
CLAYOUT1 = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
"""

LAYOUT2 = """#############
#...........#
###D#D#C#B###
  #D#C#B#A#
  #D#B#A#C#
  #B#A#A#C#
  #########
"""

class Hallway():
  def __init__(self, initialLayout, maxScore):
    self.costs = {
      'A': 1,
      'B': 10,
      'C': 100,
      'D': 1000,
    }
    self.initialCells, self.maxY, self.maxX = self.parseLayout(initialLayout)
    self.maxScore = maxScore
    
    self.currentMovelists = [(self.minRemainingCost(self.initialCells), [])]
    
    self.winningPaths = []
    
  def parseLayout(self, initialLayout):
    rows = initialLayout.split('\n')
    hallwayLength = rows[1].count('.')
    roomLength = len(rows) - 3
    
    cells = {}
    for x in range(hallwayLength):
      cells[(x, 0)] = '.'
      
    for row in range(1, roomLength+1):
      for col, cell in enumerate(rows[row+1]):
        if cell in 'ABCD':
          cells[(col-1, row)] = cell
          
    return cells, roomLength, hallwayLength
  
  def printState(self, state):
    out = '#' * (self.maxX+2) + '\n'
    out += '#' + ''.join(state[cell] for cell in state if cell[1] == 0) + '#' + '\n'
    out += '###' + '#'.join(state[cell] for cell in state if cell[1] == 1) + '###' + '\n'
    for row in range(2, self.maxY):
      out += '  #' + '#'.join(state[cell] for cell in state if cell[1] == row) + '#  ' + '\n'
    out += '  ' + '#' * (self.maxX-2) + '\n'
    
    print(out)
  
  def roomCells(self):
    roomCells = []
    for x in (2,4,6,8):
      for y in range(1, self.maxY):
        roomCells.append((x,y))
    return roomCells
  
  def roomIsCorrect(self, state, cell):
    if cell[1] == 0:
      return False
    roomType = 'ABCD'[cell[0]//2-1]
    return state[cell] == roomType
  
  def allRoomsCorrect(self, state):
    for cell in self.roomCells():
      if not self.roomIsCorrect(state, cell):
        return False
    return True
  
  def allCellsCorrect(self, state):
    for cell, pod in state.items():
      if cell[1] == 0:
        if pod != '.':
          return False
      elif cell[0] == 2:
        if pod != 'A':
          return False
      elif cell[0] == 4:
        if pod != 'B':
          return False
      elif cell[0] == 6:
        if pod != 'C':
          return False
      elif cell[0] == 8:
        if pod != 'D':
          return False
    
    return True
  
  def calculateScore(self, moves):
    return sum(self.costs[podType] * moves[podType] for podType in 'ABCD')
  
  def moveDistance(self, startingCell, targetCell):
    return startingCell[1] + abs(targetCell[0] - startingCell[0]) + targetCell[1]
  
  def doMove(self, state, move):
    startingCell, destinationCell = move
    state[destinationCell] = state[startingCell]
    state[startingCell] = '.'
    return state, state[destinationCell], self.moveDistance(startingCell, destinationCell)
  
  def computeStateFromMovelist(self, movelist):
    state = self.initialCells.copy()
    moves = {
      'A': 0,
      'B': 0,
      'C': 0,
      'D': 0,
    }
    
    for move in movelist:
      state, podType, distance = self.doMove(state, move)
      moves[podType] += distance
    
    return (self.calculateScore(moves), state)
  
  def minRemainingCost(self, state):
    nextRoom = {
      'A': (2, self.maxY-1),
      'B': (4, self.maxY-1),
      'C': (6, self.maxY-1),
      'D': (8, self.maxY-1)
    }
    
    totalRemainingCost = 0
    
    for cell in sorted(state.keys(), key=lambda x: (x[1], x[0]), reverse=True):
      podType = state[cell]
      if podType != '.':
        if cell[0] != nextRoom[podType][0]:
          totalRemainingCost += self.moveDistance(cell, nextRoom[podType]) * self.costs[podType]
        else:
          for y in range(cell[1], self.maxY):
            if state[(cell[0], y)] != podType:
              totalRemainingCost += self.moveDistance(cell, (nextRoom[podType][0]-1, 0)) * self.costs[podType]
              totalRemainingCost += self.moveDistance((nextRoom[podType][0]-1, 0), nextRoom[podType]) * self.costs[podType]
        nextRoom[podType] = (nextRoom[podType][0], nextRoom[podType][1]-1)
    return totalRemainingCost
  
  def doMoveInState(self, state, currentScore, move):
    newState = state.copy()
    
    newState, podType, distance = self.doMove(newState, move)
    
    newScore = currentScore + self.costs[podType] * distance
    predictedScore = newScore + self.minRemainingCost(newState)
      
    return (predictedScore, newState)
  
  def cellOutsideRoom(self, cell):
    return cell[1] == 0 and cell[0] in (2,4,6,8)
  
  def cellInHall(self, cell):
    return cell[1] == 0
  
  def cellInRoom(self, cell):
    return cell[1] > 0
  
  def cellIsFree(self, state, cell):
    return state[cell] == '.'
  
  def roomIsValid(self, podType, cell):
    if podType == 'A':
      return cell[0] == 2 and self.cellInRoom(cell)
    if podType == 'B':
      return cell[0] == 4 and self.cellInRoom(cell)
    if podType == 'C':
      return cell[0] == 6 and self.cellInRoom(cell)
    if podType == 'D':
      return cell[0] == 8 and self.cellInRoom(cell)
  
  def podCanLeaveRoom(self, state, cell):
    if cell[1] == 1:
      return True
    for y in range(0, cell[1]):
      if state[(cell[0], y)] != '.':
        return False
    return True
  
  def podCanMove(self, state, cell):
    return self.cellInHall(cell) or self.podCanLeaveRoom(state, cell)
  
  def pathEmpty(self, state, startingCell, targetCell):
    # Check all moves to hall (y == 0)
    x = startingCell[0]
    for y in range(startingCell[1], -1, -1):
      if (x, y) == startingCell:
        continue
      if state[(x, y)] != '.':
        return False
      
    # Check moves to correct col (x == targetCell[0])
    y = 0
    if startingCell[0] < targetCell[0]:
      for x in range(startingCell[0], targetCell[0]+1):
        if (x, y) == startingCell:
          continue
        if state[(x,y)] != '.':
          return False
    else:
      for x in range(startingCell[0], targetCell[0]-1, -1):
        if (x, y) == startingCell:
          continue
        if state[(x,y)] != '.':
          return False
        
    # Check moves down (y == targetCell[1])
    x = targetCell[0]
    for y in range(targetCell[1]+1):
      if (x, y) == startingCell:
        continue
      if state[(x,y)] != '.':
        return False
      
    return True

  def targetValid(self, state, podType, startingCell, targetCell):
    if self.cellInRoom(startingCell):
      return self.cellIsFree(state, targetCell) and (self.cellInHall(targetCell) or self.roomIsValid(podType, targetCell))
    return self.cellIsFree(state, targetCell) and self.roomIsValid(podType, targetCell)

  def podCanEnterRoom(self, state, podType, target):
    for y in range(target[1], self.maxY):
      if state[(target[0], y)] not in ('.', podType):
        return False
    return True

  def findValidMoves(self, state):
    validMoves = []
    
    allDestinationCells = [c for c in state.keys() if state[c] == '.' and not self.cellOutsideRoom(c)]
    allMovablePods = [c for c in state.keys() if state[c] != '.' and self.podCanMove(state, c)]
    for pod in allMovablePods:
      for target in allDestinationCells:
        podType = state[pod]
        if self.pathEmpty(state, pod, target) and self.targetValid(state, podType, pod, target):
          if self.cellInHall(pod) and self.cellInRoom(target):
            # validate that all lower cells are correct
            if self.podCanEnterRoom(state, podType, target):
              validMoves.append((pod, target))
          else:
            validMoves.append((pod, target))
    
    return validMoves
  
  def nextStep(self, step):
    predictedScore, bestMovelist = heappop(self.currentMovelists)
    totalScore, currentState = self.computeStateFromMovelist(bestMovelist)
    
    if step > 0 and len(self.currentMovelists) == 0:
      print(predictedScore)
      print(bestMovelist)
      print(totalScore)
      self.printState(currentState)
      print('Oh no')
    
    if self.allCellsCorrect(currentState):
      print()
      print(bestMovelist)
      print('Best score:', totalScore)
      self.printState(currentState)
      print()
      
      self.winningPaths.append((totalScore, bestMovelist, currentState))
      
      return False
    
    if not step % 10000:
      print(step, len(self.currentMovelists), predictedScore)
    
    validMoves = self.findValidMoves(currentState)
    
    for move in validMoves:
      newPredictedScore, _ = self.doMoveInState(currentState, totalScore, move)
      if newPredictedScore <= self.maxScore:
        newMovelist = bestMovelist.copy()
        newMovelist.append(move)
        heappush(self.currentMovelists, (newPredictedScore, newMovelist))
      
    return len(self.currentMovelists) > 0
  
  def solve(self):
    step = 0
    cont = self.nextStep(step)
    while cont:
      step += 1
      cont = self.nextStep(step)
      
test = Hallway(CLAYOUT1, 0)
if not test.allCellsCorrect(test.initialCells):
  print('somethings fucky')
else:
  hall = Hallway(LAYOUT1, 16300)
  hall.solve()
  
  print(min(hall.winningPaths))

  hall2 = Hallway(LAYOUT2, 43723)
  hall2.solve()
  
  print(min(hall2.winningPaths))
  
# Part 1: 16157

# Part 2: 42139	minimum, 43723 too high 43381 too low, 43881 too high