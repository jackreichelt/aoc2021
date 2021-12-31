#!/usr/bin/env python3
from math import ceil, floor

class ALU():
  def __init__(self, inputs):
    self.inputs = inputs
    self.inPointer = 0
    self.w = 0
    self.x = 0
    self.y = 0
    self.z = 0
    
  def __str__(self):
    return f'w: {self.w}, x:{self.x}, y:{self.y}, z:{self.z}'
  
  def reset(self, inputs):
    self.inputs = inputs
    self.inPointer = 0
    self.w = 0
    self.x = 0
    self.y = 0
    self.z = 0
    
  def runProgram(self, program):
    for inst in program:
      self.parseInstruction(inst)
      
  def parseInstruction(self, inst):
    op, args = inst.split(' ', maxsplit=1)
    
    opFunctions = {
      'inp': self.inp,
      'add': self.add,
      'mul': self.mul,
      'div': self.div,
      'mod': self.mod,
      'eql': self.eql
    }
    
    opFunctions[op](args)
    
  def isRegister(self, reg):
    return reg in 'wxyz'
  
  def getRegister(self, reg):
    if reg == 'w':
      return self.w
    if reg == 'x':
      return self.x
    if reg == 'y':
      return self.y
    if reg == 'z':
      return self.z
    
  def setRegister(self, reg, val):
    if reg == 'w':
      self.w = val
    if reg == 'x':
      self.x = val
    if reg == 'y':
      self.y = val
    if reg == 'z':
      self.z = val
      
  def inp(self, args):
    a = args
    val = int(self.inputs[self.inPointer])
    self.setRegister(a, val)
    self.inPointer += 1
    
  def add(self, args):
    a, b = args.split(' ')
    val = self.getRegister(a)
    if self.isRegister(b):
      val += self.getRegister(b)
    else:
      val += int(b)
    self.setRegister(a, val)
    
  def mul(self, args):
    a, b = args.split(' ')
    val = self.getRegister(a)
    if self.isRegister(b):
      val *= self.getRegister(b)
    else:
      val *= int(b)
    self.setRegister(a, val)
    
  def div(self, args):
    a, b = args.split(' ')
    val = self.getRegister(a)
    if self.isRegister(b):
      val = val // self.getRegister(b)
    else:
      val = val // int(b)
    self.setRegister(a, val)
    
  def mod(self, args):
    a, b = args.split(' ')
    val = self.getRegister(a)
    if self.isRegister(b):
      val = val % self.getRegister(b)
    else:
      val = val % int(b)
    self.setRegister(a, val)
    
  def eql(self, args):
    a, b = args.split(' ')
    valA = self.getRegister(a)
    if self.isRegister(b):
      valB = self.getRegister(b)
    else:
      valB = int(b)
    val = 1 if valA == valB else 0
    self.setRegister(a, val)
    
print('Tests')
alu = ALU('5')
tProg1 = [
  'inp x',
  'mul x -1'
]
alu.runProgram(tProg1)
print(alu)

alu.reset('39')
tProg2 = [
  'inp z',
  'inp x',
  'mul z 3',
  'eql z x'
]
alu.runProgram(tProg2)
print(alu)
alu.reset('19')
alu.runProgram(tProg2)
print(alu)

alu.reset('5')
tProg3 = [
  'inp w',
  'add z w',
  'mod z 2',
  'div w 2',
  'add y w',
  'mod y 2',
  'div w 2',
  'add x w',
  'mod x 2',
  'div w 2',
  'mod w 2',
]
alu.runProgram(tProg3)
print(alu)

print('Part 1:')
prog = [x.strip() for x in open('data.txt').readlines()]

#for model in range(99999999999999, 11111111111111, -1):
# inputs = str(model)
# if '0' not in inputs:
    # Treat as stack
    # push i[0] + 7
    # push i[1] + 8
    # push i[2] + 2
    # push i[3] + 11
    # pop if i[3] + 11 - 3 == i[4]
    # push i[5] + 12
    # push i[6] + 14
    # pop if i[6] + 14 - 16 == i[7]
    # push i[8] + 15
    # pop if i[8] + 15 - 8 == i[9]
    # pop if i[5] + 12 - 12 == i[10]
    # pop if i[2] + 2 - 7 == i[11]
    # pop if i[1] + 8 - 6 == i[12]
    # pop if i[0] + 7 - 11 == i[13]
    
#   conditions = [
#     int(inputs[3]) + 11 - 3 == int(inputs[4]),
#     int(inputs[6]) + 14 - 16 == int(inputs[7]),
#     int(inputs[8]) + 15 - 8 == int(inputs[9]),
#     int(inputs[5]) + 12 - 12 == int(inputs[10]),
#     int(inputs[2]) + 2 - 7 == int(inputs[11]),
#     int(inputs[1]) + 8 - 6 == int(inputs[12]),
#     int(inputs[0]) + 11 - 3 == int(inputs[13]),
#   ]
    
#   if all(conditions):
#     print('Valid model:', model)
    
possibilities = {
  0:[],
  1:[],
  2:[],
  3:[],
  4:[],
  5:[],
  6:[],
  7:[],
  8:[],
  9:[],
  10:[],
  11:[],
  12:[],
  13:[],
}

for a in range(1, 10):
  for b in range(1, 10):
    print(f'A: {a}, B: {b}')
    if a + 11 - 3 == b:
      possibilities[3].append(a)
      possibilities[4].append(b)
    if a + 14 - 16 == b:
      possibilities[6].append(a)
      possibilities[7].append(b)
    if a + 15 - 8 == b:
      possibilities[8].append(a)
      possibilities[9].append(b)
    if a + 12 - 12 == b:
      possibilities[5].append(a)
      possibilities[10].append(b)
    if a + 2 - 7 == b:
      possibilities[2].append(a)
      possibilities[11].append(b)
    if a + 8 - 6 == b:
      possibilities[1].append(a)
      possibilities[12].append(b)
    if a + 7 - 11 == b:
      possibilities[0].append(a)
      possibilities[13].append(b)

for i in range(14):
  print(max(possibilities[i]), end='')
print()

alu.reset('97919997299495')
alu.runProgram(prog)
print(alu)

# Part 1: 97919997299495
    
for i in range(14):
  print(min(possibilities[i]), end='')
print()

alu.reset('51619131181131')
alu.runProgram(prog)
print(alu)

# Part 2: 51619131181131