#!/usr/bin/env python3

data = [x.strip() for x in open('data.txt').readlines()]

class Cave():
	def __init__(self, caveId, size):
		self.id = caveId
		self.large = size
		self.neighbours = set()
		self.pathsTo = set()
	
	def connect(self, neigh):
		if neigh not in self.neighbours:
			self.neighbours.add(neigh)
			neigh.connect(self)
	
	def findPath(self, pathSoFar):
		pathSoFar.append(self)
		if self.id == 'end':
			pathString = ','.join([cave.id for cave in pathSoFar])
#			print(pathString)
			self.pathsTo.add(pathString)
			return
		else:
			[neigh.findPath(pathSoFar.copy()) for neigh in self.neighbours if neigh.large or neigh not in pathSoFar]
	
	def findLongerPath(self, pathSoFar, doubleDone):
		pathSoFar.append(self)
		if self.id == 'end':
			pathString = ','.join([cave.id for cave in pathSoFar])
#			print(pathString)
			self.pathsTo.add(pathString)
			return
		else:
			shortPaths = [neigh.findLongerPath(pathSoFar.copy(), doubleDone) for neigh in self.neighbours if neigh.large or neigh not in pathSoFar]
			if not doubleDone:
				longPaths = [neigh.findLongerPath(pathSoFar.copy(), True) for neigh in self.neighbours if neigh.large == False and pathSoFar.count(neigh) == 1 and neigh.id != 'start']
			

allCaves = {}

for line in data:
	cave1, cave2 = line.split('-')
	if cave1 not in allCaves.keys():
		allCaves[cave1] = Cave(cave1, cave1.isupper())
	if cave2 not in allCaves.keys():
		allCaves[cave2] = Cave(cave2, cave2.isupper())
	allCaves[cave1].connect(allCaves[cave2])

#paths = allCaves['start'].findPath([])
#
#print('Total paths:', len(allCaves['end'].pathsTo))

allCaves['end'].pathCount = 0

longPaths = paths = allCaves['start'].findLongerPath([], False)

print('Total long paths:', len(allCaves['end'].pathsTo))
