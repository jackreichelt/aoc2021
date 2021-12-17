#!/usr/bin/env python3

'target area: x=20..30, y=-10..-5'
TEST_AREA = (20, 30, -10, -5)
'target area: x=195..238, y=-93..-67'
DATA_AREA = (195, 238, -93, -67)

class Probe():
	
	def __init__(self, dx, dy, targetArea):
		self.dx = dx
		self.dy = dy # -ve is down
		self.x = 0
		self.y = 0
		self.time = 0
		self.area = targetArea
		self.maxHeight = 0
	
	def step(self):
		self.time += 1
		
		
		self.x += self.dx
		if self.dx > 0:
			self.dx -= 1
		elif self.dx < 0:
			self.dx += 1
			
		self.y += self.dy
		self.dy -= 1
		self.maxHeight = max(self.maxHeight, self.y)
	
	def isInArea(self):
		minX, maxX, minY, maxY = self.area
		return minX <= self.x <= maxX and minY <= self.y <= maxY
	
	def isTooFar(self):
		minX, maxX, minY, maxY = self.area
		if self.y < minY or self.x > maxX:
			return True
		return False
	
	def checkPath(self):
		while not self.isTooFar() and not self.isInArea():
			self.step()
		if self.isInArea():
			return True
		return False

hitTests = [Probe(7, 2, TEST_AREA), Probe(6, 3, TEST_AREA), Probe(9,0, TEST_AREA), Probe(6, 9, TEST_AREA)]
missTests = [Probe(17, -4, TEST_AREA)]

if all([p.checkPath() for p in hitTests]) and not any([p.checkPath() for p in missTests]):
	if max([p.maxHeight for p in hitTests]) == 45:
		print(hitTests[3].x, hitTests[3].y, hitTests[3].time)
		print('Max height test correct')
	else:
		print('Max height test failing')
	print('Tests pass')
else:
	print('At least one test is failing')

goodProbes = []
for dy in range(-1000, 1000):
	for dx in range(1000):
		newProbe = Probe(dx, dy, DATA_AREA)
		if newProbe.checkPath():
			goodProbes.append(newProbe)

goodProbes.sort(key = lambda p: p.maxHeight)

print(goodProbes[0].maxHeight)
print(goodProbes[-1].maxHeight)

print(len(goodProbes))