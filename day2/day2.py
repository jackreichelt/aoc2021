#!/usr/bin/env python3

instructions = [x.strip().split(' ') for x in open('data.txt').readlines()]

depth = 0
pos = 0
aim = 0

for direction, distance in instructions:
	distance = int(distance)
	if direction == 'forward':
		pos += distance
		depth += aim * distance
	elif direction == 'down':
#		depth += distance
		aim += distance
	elif direction == 'up':
#		depth -= distance
		aim -= distance
#	print(f'depth: {depth}, pos: {pos}, aim: {aim}')
	
print(depth*pos) # part 1: 1698735
# part 2: 1594785890