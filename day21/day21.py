#!/usr/bin/env python3
from collections import defaultdict

TEST = (3,7)
DATA = (5,1)

class PracticeDice():
  
  def __init__(self):
    self.current = 1
    self.timesRolled = 0
    
  def roll(self):
    val = self.current
    self.current += 1
    self.timesRolled += 1
    if self.current > 100:
      self.current == 1
    return val
  
  def roll3(self):
    return self.roll() + self.roll() + self.roll()
  
current = 0
places = list(DATA)
points = [0,0]

die = PracticeDice()

while all(p<1000 for p in points):
  places[current] = (places[current] + die.roll3()) % 10
  points[current] += places[current] + 1
  current = 1-current
  
print(points)

print('Game score:', min(points)*die.timesRolled)

#class DiracDice():
# def __init__(self, current, places, points):
#   self.current = current
#   self.places = places
#   self.points = points
#   
# def turn(self):
#   finishedGames = []
#   qGames = []
#   subCurrent = 1-self.current
#   for totalRoll in [3,4,5,6,7,8,9]:
#     subPlaces = self.places.copy()
#     subPlaces[self.current] = (places[self.current] + totalRoll) % 10
#     subPoints = self.points.copy()
#     subPoints[self.current] += subPlaces[self.current] + 1
#     if all(p<1000 for p in subPoints):
#       qGames.append(DiracDice(subCurrent, subPlaces, subPoints))
#     else:
#       finishedGames.append(DiracDice(subCurrent, subPlaces, subPoints))
#   return qGames, finishedGames
# 
# def winner(self):
#   if self.points[0] >= 21:
#     return 0
#   if self.points[1] >= 21:
#     return 1
#   return -1
# 
# 
#current = 0
#places = TEST
#points = [0,0]
#
#finishedGames = []
#qGames = [DiracDice(current, places, points)]
#
#while len(qGames) > 0:
# newQGames = []
# for g in qGames:
#   ng, fg = g.turn()
#   newQGames += ng
#   finishedGames += fg
# qGames = newQGames
#
#player2Wins = sum(g.winner() for g in finishedGames)
#player1Wins = len(finishedGames) - player2Wins
#print(f'Player 1 wins: {player1Wins}')
#print(f'Player 2 wins: {player2Wins}')

current = 0
places = DATA
points = (0,0)

def generateGames(game, count):
  outcomes = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
  
  sCurrent, sPlaces, sPoints = game
  sPlaces = list(sPlaces)
  sPoints = list(sPoints)
  
  newCurrent = 1 - sCurrent
  newGames = {}
  finishedGames = defaultdict(int)
  
  for roll, mult in outcomes.items():
    newPlaces = sPlaces.copy()
    newPlaces[sCurrent] = (sPlaces[sCurrent] + roll) % 10
    newPoints = sPoints.copy()
    newPoints[sCurrent] += newPlaces[sCurrent] + 1
    if any(p >= 21 for p in newPoints):
      if newPoints[0] >= 21:
        finishedGames[0] += count*mult
      else:
        finishedGames[1] += count*mult
    else:
      ng = (newCurrent, tuple(newPlaces), tuple(newPoints))
      newGames[ng] = count*mult
  
  return newGames, finishedGames

qGames = {(current, places, points): 1}
allFinished = defaultdict(int)
newGames = defaultdict(int)
while len(qGames) > 0:
  for game, count in qGames.items():
    results, finishedGames = generateGames(game, count)
    for ng, count in results.items():
      newGames[ng] += count
    allFinished[0] += finishedGames[0]
    allFinished[1] += finishedGames[1]
    
  qGames = newGames
  newGames = defaultdict(int)

print(max(allFinished.values()))