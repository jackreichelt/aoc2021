#!/usr/bin/env python3

data = [x.strip() for x in open('data.txt').readlines()]
template = data[0]
polyRules = {key: key[0]+insertion+key[1] for key, insertion in [pair.split(' -> ') for pair in data[2:]]}

#def polymerise(polymer, polyRules):
#	newPoly = polymer[0]
#	for index, element in enumerate(polymer[:-1]):
#		pair = element + polymer[index+1]
#		newPoly += polyRules.get(pair, pair)[1:]
#	return newPoly
#
#polymer = template
#for i in range(10):
#	polymer = polymerise(polymer, polyRules)
#
#maxElementName = max(polymer, key=lambda key: polymer.count(key))
#minElementName = min(polymer, key=lambda key: polymer.count(key))
#maxElementCount = polymer.count(maxElementName)
#minElementCount = polymer.count(minElementName)
#print('Element with max:', maxElementName, maxElementCount)
#print('Element with min:', minElementName, minElementCount)
#print(maxElementCount - minElementCount) # Part 1: 2590

def findPairs(polymer):
	polymerPairs = {}
	for index, element in enumerate(polymer[:-1]):
		pair = element + polymer[index+1]
		polymerPairs[pair] = polymerPairs.get(pair, 0)+1
	return polymerPairs

def smartPolymerise(polymerPairs, polyRules, polyHist):
	newPolyPairs = polymerPairs.copy()
	for pair, count in polymerPairs.items():
		if count:
			newPair1 = polyRules[pair][0:2]
			newPair2 = polyRules[pair][1:]
			newPolyPairs[pair] = newPolyPairs[pair] - count
			newPolyPairs[newPair1] = newPolyPairs.get(newPair1, 0) + count
			newPolyPairs[newPair2] = newPolyPairs.get(newPair2, 0) + count
			polyHist[polyRules[pair][1]] = polyHist.get(polyRules[pair][1], 0) + count
	return newPolyPairs, polyHist


polymer = findPairs(template)
polyHist = {e: template.count(e) for e in set(template)}
for i in range(40):
	polymer, polyHist = smartPolymerise(polymer, polyRules, polyHist)
	if i == 9:
		maxElementName = max(polyHist, key=lambda key: polyHist[key])
		minElementName = min(polyHist, key=lambda key: polyHist[key])
		maxElementCount = polyHist[maxElementName]
		minElementCount = polyHist[minElementName]
		print('Element with max:', maxElementName, maxElementCount)
		print('Element with min:', minElementName, minElementCount)
		print(maxElementCount - minElementCount) # Part 1: 2590

maxElementName = max(polyHist, key=lambda key: polyHist[key])
minElementName = min(polyHist, key=lambda key: polyHist[key])
maxElementCount = polyHist[maxElementName]
minElementCount = polyHist[minElementName]
print('Element with max:', maxElementName, maxElementCount)
print('Element with min:', minElementName, minElementCount)
print(maxElementCount - minElementCount) # Part 2: 2875665202438