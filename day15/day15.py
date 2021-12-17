#!/usr/bin/env python3
from sys import maxsize
from heapq import heappush, heappop

chitonDensity = [[int(cell) for cell in row.strip()] for row in open('data.txt').readlines()]

def bigify(densityMap):
	maxIndex = len(densityMap)
	
	bigMap = []
	for yTile in range(5):
		for y in range(maxIndex):
			bigMap.append([])
			for xTile in range(5):
				for x in range(maxIndex):
					newRisk = densityMap[y][x]+xTile+yTile
					if newRisk > 9:
						newRisk = newRisk % 10 + 1
					bigMap[yTile*maxIndex + y].append(newRisk)
	return bigMap

def findAdjacents(cell):
	x, y = cell
	adjacents = []
	if x-1 >= 0:
		adjacents.append((x-1, y))
	if x+1 <= maxIndex:
		adjacents.append((x+1, y))
	if y-1 >= 0:
		adjacents.append((x, y-1))
	if y+1 <= maxIndex:
		adjacents.append((x, y+1))
	return adjacents

def cellRisk(cell):
	return chitonDensity[cell[1]][cell[0]]

chitonDensity = bigify(chitonDensity)

maxIndex = len(chitonDensity)-1
start = (0, 0)
end = (maxIndex, maxIndex)

lowestRisk = {}
cellsChecked = set()

checkingQueue = []

risk = 0
cell = start
while cell != end:
	cellsChecked.add(cell)
	adjacents = findAdjacents(cell)
	
	for a in adjacents:
		if a not in cellsChecked:
			newRisk = risk + cellRisk(a)
			if newRisk < lowestRisk.get(a, maxsize):
				lowestRisk[a] = newRisk
				heappush(checkingQueue, (newRisk, a))
	
	risk, cell = heappop(checkingQueue)

print('Total risk:', risk)