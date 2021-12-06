#!/usr/bin/env python3

initialFish = [int(x) for x in open('data.txt').readline().strip().split(',')]

def dayStep(fish):
	spawners = fish.count(0)
	
	newFish = [f-1 for f in fish if f != 0]
	newFish += [8] * spawners
	newFish += [6] * spawners
	
	return newFish

fish = initialFish
for i in range(80):
	fish = dayStep(fish)

print(len(fish)) # part 1: 362639

fishHist = {num: initialFish.count(num) for num in set(initialFish)}

for day in range(256):
	spawners = fishHist.get(0, 0)
	fishHist = {age: fishHist.get(age+1, 0) for age in range(8)}
	fishHist[6] = fishHist.get(6, 0) + spawners
	fishHist[8] = spawners

print(sum(fishHist.values())) # part 2: 1639854996917