#!/usr/bin/env python3

initialCrabs = [int(x) for x in open('data.txt').readline().strip().split(',')]

def alignmentFuelCost(crabs, target):
	return sum([abs(crab-target) for crab in crabs])

def increasingFuelCost(crabs, target):
	return sum([(abs(crab-target))*(abs(crab-target)+1)//2 for crab in crabs])
		
minCost = len(initialCrabs)*max(initialCrabs)
bestTarget = -1
for i in range(min(initialCrabs), max(initialCrabs)):
	alignmentCost = alignmentFuelCost(initialCrabs, i)
	if alignmentCost < minCost:
		minCost = alignmentCost
		bestTarget = i
	
print(f'Best target is {bestTarget} costing {minCost}.')

minCost = (len(initialCrabs)*max(initialCrabs))**2
bestTarget = -1
for i in range(min(initialCrabs), max(initialCrabs)):
	alignmentCost = increasingFuelCost(initialCrabs, i)
	if alignmentCost < minCost:
		minCost = alignmentCost
		bestTarget = i
		
print(f'Best real target is {bestTarget} costing {minCost}.')