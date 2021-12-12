#!/usr/bin/env python3

nums = [int(x.strip()) for x in open('data.txt').readlines()]
count = 0
prevSum = max(nums)*3
window = [nums[0], nums[1]]
for i in nums[2:]:
  window.append(i)
  if sum(window) > prevSum:
    count += 1
  prevSum = sum(window)
  window.pop(0)
print(count)
