#!/usr/bin/env python3
from statistics import mode

nums = [x.strip() for x in open('data.txt').readlines()]

def powerConsumption(gamma, epsilon):
	return int(gamma, 2) * int(epsilon, 2)

def gammaBit(bits):
	return mode(bits)

def epsilonBit(bits):
	return 1 - mode(bits)

gammaString = ''
epsilonString = ''

for i in range(len(nums[0])):
	gammaString += str(gammaBit([int(num[i]) for num in nums]))
	epsilonString += str(epsilonBit([int(num[i]) for num in nums]))

print(powerConsumption(gammaString, epsilonString)) # part 1 2583164

def lifeSupport(o2, co2):
	return int(o2, 2) * int(co2, 2)

def o2Rating(nums):
	for i in range(len(nums[0])):
		bits = [int(num[i]) for num in nums]
		filterBit = str(mode(bits))
		if bits.count(0) == bits.count(1):
			filterBit = '1'
		nums = [x for x in filter(lambda x : x[i] == filterBit, nums)]
		if len(nums) == 1:
			return nums[0]
	
def co2Rating(nums):
	for i in range(len(nums[0])):
		bits = [int(num[i]) for num in nums]
		filterBit = str(1 - mode(bits))
		if bits.count(0) == bits.count(1):
			filterBit = '0'
		nums = [x for x in filter(lambda x : x[i] == filterBit, nums)]
		if len(nums) == 1:
			return nums[0]
		
o2R = o2Rating(nums)
co2R = co2Rating(nums)
print(o2R, co2R)
print(lifeSupport(o2R, co2R)) # 2784375