#!/usr/bin/env python3
from math import prod

HEIGHTMAP = [[int(point) for point in x.strip()] for x in open('data.txt').readlines()]

MAX_X = len(HEIGHTMAP[0])
MAX_Y = len(HEIGHTMAP)

def findAdjacents(x, y):
	adjacents = []
	if x-1 >= 0:
		adjacents.append((x-1, y))
	if x+1 < MAX_X:
		adjacents.append((x+1, y))
	if y-1 >= 0:
		adjacents.append((x, y-1))
	if y+1 < MAX_Y:
		adjacents.append((x, y+1))
	return adjacents

def findHigherAdjacents(pointX, pointY, pointVal):
	highers = []
	adjacents = findAdjacents(pointX, pointY)
	for x, y in adjacents:
		adjHeight = HEIGHTMAP[y][x]
		if adjHeight != 9 and adjHeight > pointVal:
			highers.append((x, y))
	return highers

def isLow(point, adjacents):
	return all([point < HEIGHTMAP[y][x] for x, y in adjacents])

def findBasin(lowX, lowY):
	basinPoints = set()
	pointsToCheck = [(lowX, lowY)]
	
	for x, y in pointsToCheck:
		basinPoints.add((x, y))
		pointsToCheck += findHigherAdjacents(x, y, HEIGHTMAP[y][x])
		
	return len(basinPoints)

lowSum = 0
basinSizes = []

for y, row in enumerate(HEIGHTMAP):
	for x, point in enumerate(row):
		adjacents = findAdjacents(x, y)
		if isLow(point, adjacents):
			lowSum += point + 1
			basinSizes.append(findBasin(x, y))
			
bigBasins = sorted(basinSizes)[-3:]
	
print(lowSum) # part 1: 631
print(prod(bigBasins)) # part 2: 821560