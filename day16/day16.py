#!/usr/bin/env python3
from math import prod

def hexToBinString(hexStr):
  decNum = int(hexStr, 16)
  binStr = format(decNum, "b")
  return '0' * (len(hexStr)*4 - len(binStr)) + binStr


dataPointer = 0

def advancePointer(dataPointer):
  if dataPointer % 4 == 0:
    return dataPointer
  return (dataPointer//4+1)*4

def getSnippet(binary, dataPointer, length):
  return binary[dataPointer:dataPointer+length], dataPointer+length

def getVersion(binary, dataPointer):
  return getSnippet(binary, dataPointer, 3)

def getType(binary, dataPointer):
  return getSnippet(binary, dataPointer, 3)

def getLengthTypeId(binary, dataPointer):
  return getSnippet(binary, dataPointer, 1)

def getBitLength(binary, dataPointer):
  return getSnippet(binary, dataPointer, 15)

def getPacketCount(binary, dataPointer):
  return getSnippet(binary, dataPointer, 11)

def readAheadType(binary, dataPointer):
  packetType, _ = getType(binary, dataPointer + 3)
  return packetType

def getLiteralValue(binary, dataPointer):
  chunk, dataPointer = getSnippet(binary, dataPointer, 5)
  continueBit = chunk[0]
  number = chunk[1:]
  while continueBit == '1':
    chunk, dataPointer = getSnippet(binary, dataPointer, 5)
    continueBit = chunk[0]
    number += chunk[1:]
  return int(number, 2), dataPointer

def getValuePacket(binary, dataPointer):
  start = dataPointer
  version, dataPointer = getVersion(binary, dataPointer)
  packetType, dataPointer = getType(binary, dataPointer)
  value, dataPointer = getLiteralValue(binary, dataPointer)
  
  if int(packetType, 2) != 4:
    print(f'Error reading packet from {start} to {dataPointer}! Expected packetType 4, got {int(packetType, 2)}!')
    exit()  
  return int(version, 2), packetType, value, dataPointer

def getLengthOfPackets(binary, dataPointer):
  bitLength, dataPointer = getBitLength(binary, dataPointer)
  targetPointer = dataPointer + int(bitLength, 2)
  
  versionSum = 0
  values = []
  while dataPointer < targetPointer:
    version, packetType, thisValue, dataPointer = parseBinary(binary, dataPointer)
    versionSum += version
    values.append(thisValue)
  
  if dataPointer > targetPointer:
    print(f'Error reading {int(bitLength, 2)} bits of packets. Read {int(bitLength, 2) + dataPointer - targetPointer} instead.')
    print(f'Values so far', ', '.join([str(x) for x in values]))
  
  return versionSum, values, dataPointer

def getNumberOfPackets(binary, dataPointer):
  packetCountBin, dataPointer = getPacketCount(binary, dataPointer)
  packetCount = int(packetCountBin, 2)
  
  versionSum = 0
  values = []
  for i in range(packetCount):
    version, packetType, thisValue, dataPointer = parseBinary(binary, dataPointer)
    versionSum += version
    values.append(thisValue)
      
  return versionSum, values, dataPointer

def getOperatorPacketAndValues(binary, dataPointer):
  version, dataPointer = getVersion(binary, dataPointer)
  packetType, dataPointer = getType(binary, dataPointer)
  lengthType, dataPointer = getLengthTypeId(binary, dataPointer)
  
  if lengthType == '0':
    versionSum, values, dataPointer = getLengthOfPackets(binary, dataPointer)
  elif lengthType == '1':
    versionSum, values, dataPointer = getNumberOfPackets(binary, dataPointer)
  return versionSum+int(version, 2), packetType, values, dataPointer

def parseBinary(binary, dataPointer):
  start = dataPointer
  packetType = int(readAheadType(binary, dataPointer), 2)
  if packetType == 0:
    versionSum, packetType, values, dataPointer = getOperatorPacketAndValues(binary, dataPointer)
    return versionSum, packetType, sum(values), dataPointer
  elif packetType == 1:
    versionSum, packetType, values, dataPointer = getOperatorPacketAndValues(binary, dataPointer)
    return versionSum, packetType, prod(values), dataPointer
  elif packetType == 2:
    versionSum, packetType, values, dataPointer = getOperatorPacketAndValues(binary, dataPointer)
    return versionSum, packetType, min(values), dataPointer
  elif packetType == 3:
    versionSum, packetType, values, dataPointer = getOperatorPacketAndValues(binary, dataPointer)
    return versionSum, packetType, max(values), dataPointer
  elif packetType == 4:
    return getValuePacket(binary, dataPointer)
  elif packetType == 5:
    versionSum, packetType, values, dataPointer = getOperatorPacketAndValues(binary, dataPointer)
    return versionSum, packetType, 1 if values[0] > values[1] else 0, dataPointer
  elif packetType == 6:
    versionSum, packetType, values, dataPointer = getOperatorPacketAndValues(binary, dataPointer)
    return versionSum, packetType, 1 if values[0] < values[1] else 0, dataPointer
  elif packetType == 7:
    versionSum, packetType, values, dataPointer = getOperatorPacketAndValues(binary, dataPointer)
    return versionSum, packetType, 1 if values[0] == values[1] else 0, dataPointer
  else: 
    print(f'Invalid packet type {packetType} for packet {start}:{dataPointer}')
    exit()

def parsePacket(hexStr):
  binStr = hexToBinString(hexStr)
  return parseBinary(binStr, 0)

def test1():
  hexStr = 'D2FE28'
  binStr = hexToBinString(hexStr)
  if binStr != '110100101111111000101000':
    print('Conversion wrong')
    return False
  
  testPointer = 0
  version, testPointer = getVersion(binStr, testPointer)
  if int(version, 2) != 6 or testPointer != 3:
    print('Version wrong')
    return False
  
  packetType, testPointer = getType(binStr, testPointer)
  if int(packetType, 2) != 4 or testPointer != 6:
    print('Type wrong')
    return False
  
  value, testPointer = getLiteralValue(binStr, testPointer)
  if value != 2021 or testPointer != 21:
    print('Value wrong')
    return False
  
  version, packetType, value, testPointer = getValuePacket(binStr, 0)
  if version != 6 or value != 2021 or testPointer != 21:
    print('Packet parsing wrong')
    return False
  
  print('Test 1 passes!')
  return True

def test2():
  hexStr = '38006F45291200'
  binStr = hexToBinString(hexStr)
  if binStr != '00111000000000000110111101000101001010010001001000000000':
    print('Conversion wrong')
    return False
  
  testPointer = 0
  version, testPointer = getVersion(binStr, testPointer)
  if int(version, 2) != 1 or testPointer != 3:
    print('Version wrong')
    return False
  
  packetType, testPointer = getType(binStr, testPointer)
  if int(packetType, 2) != 6 or testPointer != 6:
    print('Type wrong')
    return False
  
  lengthType, testPointer = getLengthTypeId(binStr, testPointer)
  if int(lengthType, 2) != 0 or testPointer != 7:
    print('Length Type wrong')
    return False
  
  bitLength, tempPointer = getBitLength(binStr, testPointer)
  if int(bitLength, 2) != 27 or tempPointer != 22:
    print('Bit length wrong')
    return False
  
  versionSum, values, testPointer = getLengthOfPackets(binStr, testPointer)
  if values != [10, 20] or testPointer != 49:
    print('Values wrong')
    return False
  
  versionSum, packetType, values, testPointer = getOperatorPacketAndValues(binStr, 0)
  if int(packetType, 2) != 6 or values != [10, 20] or testPointer != 49:
    print('Operator packet parsing wrong')
    return False
  
  print('Test 2 passes!')
  return True
  
def test3():
  hexStr = 'EE00D40C823060'
  binStr = hexToBinString(hexStr)
  if binStr != '11101110000000001101010000001100100000100011000001100000':
    print('Conversion wrong')
    return False
  
  testPointer = 0
  version, testPointer = getVersion(binStr, testPointer)
  if int(version, 2) != 7 or testPointer != 3:
    print('Version wrong')
    return False
  
  packetType, testPointer = getType(binStr, testPointer)
  if int(packetType, 2) != 3 or testPointer != 6:
    print('Type wrong')
    return False
  
  lengthType, testPointer = getLengthTypeId(binStr, testPointer)
  if int(lengthType, 2) != 1 or testPointer != 7:
    print('Length Type wrong')
    return False
  
  packetCount, tempPointer = getPacketCount(binStr, testPointer)
  if int(packetCount, 2) != 3 or tempPointer != 18:
    print('Bit length wrong')
    return False
  
  versionSum, values, testPointer = getNumberOfPackets(binStr, testPointer)
  if values != [1, 2, 3] or testPointer != 51:
    print('Values wrong')
    return False
  
  versionSum, packetType, values, testPointer = getOperatorPacketAndValues(binStr, 0)
  if int(packetType, 2) != 3 or values != [1, 2, 3] or testPointer != 51:
    print('Operator packet parsing wrong')
    return False
  
  print('Test 3 passes!')
  return True
  
def test4():
  hexStr = '8A004A801A8002F478'
  versionSum, _, _, _ = parsePacket(hexStr)
  if versionSum != 16:
    print(f'Error summing versions for {hexStr}. Expected 16 for {versionSum}')
  print('Test 4.1 passes!')
    
  hexStr = '620080001611562C8802118E34'
  versionSum, _, _, _ = parsePacket(hexStr)
  if versionSum != 12:
    print(f'Error summing versions for {hexStr}. Expected 12 for {versionSum}')
  print('Test 4.2 passes!')
    
  hexStr = 'C0015000016115A2E0802F182340'
  versionSum, _, _, _ = parsePacket(hexStr)
  if versionSum != 23:
    print(f'Error summing versions for {hexStr}. Expected 23 for {versionSum}')
  print('Test 4.3 passes!')
    
  hexStr = 'A0016C880162017C3686B18A3D4780'
  versionSum, _, _, _ = parsePacket(hexStr)
  if versionSum != 31:
    print(f'Error summing versions for {hexStr}. Expected 31 for {versionSum}')
  print('Test 4.4 passes!')
  
  print('Test 4 passes!')
  return True

def test5():
  hexStr = 'C200B40A82'
  _, _, value, _ = parsePacket(hexStr)
  if value != 3:
    print(f'Value error for {hexStr}. Expected 3 got {value}')
  print('Test 5.1 passes!')
  
  hexStr = '04005AC33890'
  _, _, value, _ = parsePacket(hexStr)
  if value != 54:
    print(f'Value error for {hexStr}. Expected 54 got {value}')
  print('Test 5.2 passes!')
  
  hexStr = '880086C3E88112'
  _, _, value, _ = parsePacket(hexStr)
  if value != 7:
    print(f'Value error for {hexStr}. Expected 7 got {value}')
  print('Test 5.3 passes!')
  
  hexStr = 'CE00C43D881120'
  _, _, value, _ = parsePacket(hexStr)
  if value != 9:
    print(f'Value error for {hexStr}. Expected 9 got {value}')
  print('Test 5.4 passes!')
  
  hexStr = 'D8005AC2A8F0'
  _, _, value, _ = parsePacket(hexStr)
  if value != 1:
    print(f'Value error for {hexStr}. Expected 1 got {value}')
  print('Test 5.5 passes!')
  
  hexStr = 'F600BC2D8F'
  _, _, value, _ = parsePacket(hexStr)
  if value != 0:
    print(f'Value error for {hexStr}. Expected 0 got {value}')
  print('Test 5.6 passes!')
  
  hexStr = '9C005AC2F8F0'
  _, _, value, _ = parsePacket(hexStr)
  if value != 0:
    print(f'Value error for {hexStr}. Expected 0 got {value}')
  print('Test 5.7 passes!')
  
  hexStr = '9C0141080250320F1802104A08'
  _, _, value, _ = parsePacket(hexStr)
  if value != 1:
    print(f'Value error for {hexStr}. Expected 1 got {value}')
  print('Test 5.8 passes!')
  
  print('Test 5 passes!')
  return True


if not all([test1(), test2(), test3(), test4(), test5()]):
  exit()
  
packets = open('data.txt').read()

versionSum, _, value, _ = parsePacket(packets)
print('Version Sum:', versionSum)
print('Value:', value)