#!/usr/bin/env python3
from statistics import median

def constructBinary(mapData, x, y):
	binString = ''
	for checkY in (y-1, y, y+1):
		for checkX in (x-1, x, x+1):
			if (checkX, checkY) in mapData:
				binString += '1'
			else:
				binString += '0'
	return binString
	
def shouldAdd(binary):
	return algorithm[int(binary, 2)] == '#'

def printMap(mapData):
	minX = min([cell[0] for cell in mapData])-1
	maxX = max([cell[0] for cell in mapData])+2
	minY = min([cell[1] for cell in mapData])-1
	maxY = max([cell[1] for cell in mapData])+2
	
	for y in range(minY, maxY):
		for x in range(minX, maxX):
			if (x,y) in mapData:
				print('#', end='')
			else:
				print('.', end='')
		print()
	print()
	
def printMapAroundPoint(mapData, x, y):
	for y in range(y-2, y+3):
		for x in range(x-2, x+3):
			if (x,y) in mapData:
				print('#', end='')
			else:
				print('.', end='')
		print()
	print()

def enhance(mapData):
	newMap = set()
	
	minX = min([cell[0] for cell in mapData])-20
	maxX = max([cell[0] for cell in mapData])+20
	minY = min([cell[1] for cell in mapData])-20
	maxY = max([cell[1] for cell in mapData])+20
	
	for x in range(minX, maxX):
		for y in range(minY, maxY):
			binary = constructBinary(mapData, x, y)
			if shouldAdd(binary):
				newMap.add((x, y))
	return newMap

def contract(mapData, bufferSize):
	if bufferSize == -1:
		return mapData
	newMap = set()
	minX = min([cell[0] for cell in mapData])+bufferSize
	maxX = max([cell[0] for cell in mapData])-bufferSize
	minY = min([cell[1] for cell in mapData])+bufferSize
	maxY = max([cell[1] for cell in mapData])-bufferSize
	
	for x in range(minX, maxX):
		for y in range(minY, maxY):
			if (x,y) in mapData:
				newMap.add((x,y))
	return newMap

def findBufferSize(mapData):
	y = median([cell[1] for cell in mapData])
	minX = min([cell[0] for cell in mapData])
	maxX = max([cell[0] for cell in mapData])
	
	bufferLen = 0
	onPrefix = 0
	for x in range(minX, maxX):
		if (x, y) in mapData:
			onPrefix += 1
		else:
			break
	
	offPrefix = 0
	for x in range(minX+onPrefix, maxX):
		if (x, y) not in mapData:
			offPrefix += 1
		else:
			break
	
	if onPrefix > 10 and offPrefix > 10:
		return onPrefix + offPrefix//2
	return -1
	
	
data = [x.strip() for x in open('data.txt').readlines()]
algorithm = data[0]
initialMap = data[2:]

mapData = set()

for y, row in enumerate(initialMap):
	for x, cell in enumerate(row):
		if cell == '#':
			mapData.add((x,y))
			
printMap(mapData)
for i in range(2):
	mapData = enhance(mapData)
	printMap(mapData)
	mapData = contract(mapData, findBufferSize(mapData))
	printMap(mapData)
	
print('Part 1:', len(mapData)) # Part 1: 5339

for i in range(48):
	mapData = enhance(mapData)
	mapData = contract(mapData, findBufferSize(mapData))
	
	
print('Part 2:', len(mapData)) # Part 2: 18395