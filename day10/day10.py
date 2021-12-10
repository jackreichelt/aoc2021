#!/usr/bin/env python3
from statistics import median
data = [x.strip() for x in open('data.txt').readlines()]

OPENERS = '([{<'
CLOSERS = ')]}>'

OPENER_MAP = {
	'(': ')',
	'[': ']',
	'{': '}',
	'<': '>',
}

CLOSER_MAP = {
	')': '(',
	']': '[',
	'}': '{',
	'>': '<',
}

ERROR_POINTS = {
	')': 3,
	']': 57,
	'}': 1197,
	'>': 25137,
}

FINISH_POINTS = {
	')': 1,
	']': 2,
	'}': 3,
	'>': 4,
}

def isCorrupted(line):
	charCounts = {
		'(': 0,
		'[': 0,
		'{': 0,
		'<': 0,
	}
	
	charStack = []
	
	for char in line:
		if char in OPENERS:
			charCounts[char] += 1
			charStack.append(char)
		else:
			charCounts[CLOSER_MAP[char]] -= 1
			if charCounts[CLOSER_MAP[char]] < 0:
				return ERROR_POINTS[char]
			if charStack.pop() != CLOSER_MAP[char]:
				return ERROR_POINTS[char]
	return 0

errorScore = sum(isCorrupted(line) for line in data)
		
print('Total error score:', errorScore)

def completeLine(line):
	charCounts = {
		'(': 0,
		'[': 0,
		'{': 0,
		'<': 0,
	}
	
	charStack = []
	
	finishScore = 0
	
	for char in line:
		if char in OPENERS:
			charCounts[char] += 1
			charStack.append(char)
		else:
			charCounts[CLOSER_MAP[char]] -= 1
			charStack.pop()
	
	for char in charStack[::-1]:
		line += OPENER_MAP[char]
		finishScore *= 5
		finishScore += FINISH_POINTS[OPENER_MAP[char]]
	
	if isCorrupted(line):
		print('something went wrong finishing line', line)
	
	return finishScore
		

incompleteLines = [line for line in data if not isCorrupted(line)]

finishScores = [completeLine(line) for line in incompleteLines]

print(median(finishScores))