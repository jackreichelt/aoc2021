#!/usr/bin/env python3
from math import floor
from statistics import mean

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

target = floor(mean(initialCrabs))
alignmentCost = increasingFuelCost(initialCrabs, target)	
print(f'Best real target is {target} costing {alignmentCost}.')