#!/usr/bin/env python3

data = [x.strip() for x in open('data.txt').readlines()]

easyNums = 0

for line in data:
  signals, values = [part.split(' ') for part in line.split(' | ')]

  easyNums += len([v for v in values if len(v) in (2,3,4,7)])

print(easyNums) # part 1: 519

total = 0

for line in data:
  possibilities = {
    'a': set('abcdefg'),
    'b': set('abcdefg'),
    'c': set('abcdefg'),
    'd': set('abcdefg'),
    'e': set('abcdefg'),
    'f': set('abcdefg'),
    'g': set('abcdefg'),
  }

  signals, values = [part.split(' ') for part in line.split(' | ')]

  sortedSignals = sorted([set(s) for s in signals], key=lambda x : len(x))

  mapping = {}

  # unique mappings
  mapping[1] = sortedSignals[0]
  mapping[4] = sortedSignals[2]
  mapping[7] = sortedSignals[1]
  mapping[8] = sortedSignals[-1]

  # deduced from difference between 7 and 1
  possibilities['a'] = mapping[7] - mapping[1]
  for seg, poss in possibilities.items():
    if seg != 'a':
      possibilities[seg] = poss - possibilities['a']

      # only 2 doesn't have segment f
  for seg in 'abcdefg':
    signalsMissing = [sig for sig in sortedSignals if seg not in sig]
    if len(signalsMissing) == 1:
      mapping[2] = signalsMissing[0]
      possibilities['f'] = set(seg)
      break
  for seg, poss in possibilities.items():
    if seg != 'f':
      possibilities[seg] = poss - possibilities['f']

      # segment c is the segment in 1 that isn't f
  possibilities['c'] = mapping[1] - possibilities['f']
  for seg, poss in possibilities.items():
    if seg != 'c':
      possibilities[seg] = poss - possibilities['c']

      # 6 is the signal that has everything except segment c
  for sig in sortedSignals:
    if len(sig) == 6 and possibilities['c'].isdisjoint(sig):
      mapping[6] = sig

      # 5 has all but signal e from 6
  for sig in sortedSignals:
    if len(sig) == 5 and len(mapping[6] - sig) == 1 and possibilities['c'] not in sig:
      mapping[5] = sig
      possibilities['e'] = mapping[6] - sig
      for seg, poss in possibilities.items():
        if seg != 'e':
          possibilities[seg] = poss - possibilities['e']

          # i now know 1, 2, 4, 5, 6, 7, 8, 0. I need to find 3, 9, 0
          # 3 is len 5, 9 and 0 are len 6
          # 9 doesn't have e, 0 does
  remaining = [sig for sig in sortedSignals if sig not in mapping.values()]
  mapping[3] = remaining[0]
  mapping[0] = remaining[1] if possibilities['e'].issubset(remaining[1]) else remaining[2]
  mapping[9] = remaining[1] if not possibilities['e'].issubset(remaining[1]) else remaining[2]

  num = ''

  for val in values:
    for digit, signal in mapping.items():
      if set(val) == signal:
        num += str(digit)

  total += int(num)

print(total) # part 2: 1027483

# better way for part 2:
total = 0

for line in data:
  signals, values = [part.split(' ') for part in line.split(' | ')]

  sortedSignals = sorted([set(s) for s in signals], key=lambda x : len(x))

  mapping = {}

  # unique mappings
  mapping[1] = sortedSignals.pop(0)
  mapping[4] = sortedSignals.pop(1) # originally 2
  mapping[7] = sortedSignals.pop(0) # originalLy 1
  mapping[8] = sortedSignals.pop(-1)

  twoThreeFive = sortedSignals[0:3]
  sixNineZero = sortedSignals[3:]

  for signal in twoThreeFive:
    if signal.issuperset(mapping[1]):
      mapping[3] = signal
    elif len(signal.intersection(mapping[4])) == 3:
      mapping[5] = signal
    else:
      mapping[2] = signal

  for signal in sixNineZero:
    if len(signal.intersection(mapping[7])) == 2:
      mapping[6] = signal
    elif signal.issuperset(mapping[4]):
      mapping[9] = signal
    else:
      mapping[0] = signal

  num = ''

  for val in values:
    for digit, signal in mapping.items():
      if set(val) == signal:
        num += str(digit)

  total += int(num)

print(total) # part 2: 1027483
