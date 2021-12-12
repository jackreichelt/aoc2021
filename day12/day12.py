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
			return pathSoFar
		else:
			return [neigh.findPath(pathSoFar.copy()) for neigh in self.neighbours if neigh.large or neigh not in pathSoFar]
	
	def findLongerPath(self, pathSoFar, doubleDone):
		pathSoFar.append(self)
		if self.id == 'end':
			pathString = ','.join([cave.id for cave in pathSoFar])
#			print(pathString)
			self.pathsTo.add(pathString)
			return
		else:
			shortPathOptions = [neigh for neigh in self.neighbours if neigh.large or neigh not in pathSoFar]
			longPathOptions = [neigh for neigh in self.neighbours if not neigh.large and neigh not in shortPathOptions and neigh.id != 'start']
			[neigh.findLongerPath(pathSoFar.copy(), doubleDone) for neigh in shortPathOptions]
			if not doubleDone:
				[neigh.findLongerPath(pathSoFar.copy(), True) for neigh in longPathOptions]

allCaves = {}

for line in data:
	cave1, cave2 = line.split('-')
	if cave1 not in allCaves.keys():
		allCaves[cave1] = Cave(cave1, cave1.isupper())
	if cave2 not in allCaves.keys():
		allCaves[cave2] = Cave(cave2, cave2.isupper())
	allCaves[cave1].connect(allCaves[cave2])

paths = allCaves['start'].findPath([])

print('Total paths:', len(allCaves['end'].pathsTo))

allCaves['end'].pathCount = 0

longPaths = paths = allCaves['start'].findLongerPath([], False)

print('Total long paths:', len(allCaves['end'].pathsTo))
