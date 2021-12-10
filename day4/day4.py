#!/usr/bin/env python3

class Bingo:

  def __init__(self, boardData):
    self.board = {} # dict mapping (x, y) => Pos instance
    for y, row in enumerate(boardData):
      for x, number in enumerate(row.strip().replace('  ', ' ').split(' ')):
        self.board[(x, y)] = Position(x, y, int(number.strip()))

  def score(self):
    return sum([x.num for x in self.board.values() if x.marked == False])

  def mark(self, num):
    for pos in self.board.values():
      if pos.num == num:
        pos.mark()

  def isDone(self):
    # check if a row is complete
    for row in range(5):
      rowMarks = []
      for col in range(5):
        rowMarks.append(self.board[col, row].marked)
      if all(rowMarks):
        return True

      # check if a col is complete
    for col in range(5):
      colMarks = []
      for row in range(5):
        colMarks.append(self.board[col, row].marked)
      if all(colMarks):
        return True

    return False

class Position:	
  def __init__(self, x, y, num):
    self.x = x
    self.y = y
    self.num = num
    self.marked = False

  def mark(self):
    self.marked = True

chunks = open('data.txt').read().split('\n\n')

nums = [int(x) for x in chunks[0].strip().split(',')]
boardData = [chunk.split('\n') for chunk in chunks[1:]]
boards = []

for board in boardData:
  boards.append(Bingo(board))

for num in nums:
  if len(boards) == 0:
    break
  for board in boards:
    board.mark(num)

  newBoards = []
  for board in boards:
    if board.isDone():
      print(f'Board is done!\nBoard score: {board.score()}\nLast num: {num}\n Total Score: {board.score() * num}')
    else:
      newBoards.append(board)

  boards = newBoards
