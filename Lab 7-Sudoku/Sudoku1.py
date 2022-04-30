# Jason Xu
# Sudoku Part 1

import sys, time, random
sizes = dict()
constraints = dict()
spaceCons = dict()


def findVals(n):
    sq = n**0.5
    if int(sq)**2 == n:
        w = int(sq)
    else:
        w = int(sq + 1)
    h = int(sq)
    if not sq**2 == n:
        while not n % w == 0:
            w = w + 1
        while not n % h == 0:
            h = h - 1
    symbols = []
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(n):
        num = i + 1
        if num < 10:
            symbols.append(str(num))
        else:
            symbols.append(alpha[num - 10])
    return w, h, symbols


def findCons(n):
    cons = []
    for row in range(n):
        horiz = set(range(row*size, (row+1)*n))
        cons.append(horiz)
    for col in range(n):
        v = col
        vert = set()
        for v in range(v, int(size**2),n):
            vert.add(v)
        cons.append(vert)
    vals = sizes[n]
    for col in range(n//vals[1]):
        for row in range(n//vals[0]):
            block = set()
            for ypos in range(vals[1]):
                for xpos in range(vals[0]):
                    block.add((col*vals[1]*n) + ypos * n + (row*vals[0]) + xpos)
            cons.append(block)
    return cons


def findNext(board):
    return board.index(".")


def getVals(board, index, n):
    possibles = set(sizes[n][2])
    cons = spaceCons[n][index]
    for val in cons:
        if board[val] in possibles:
            possibles.remove(board[val])
    return possibles


def solve(board, n):
    if check(board):
        return board
    nextPos = findNext(board)
    nextVals = getVals(board, nextPos, n)
    for val in nextVals:
        boardList = list(board)
        boardList[nextPos] = val
        result = solve("".join(boardList),n)
        if not result == None:
            return result
    return None


def check(board):
    if "." in board:
        return False
    return True

def instances(board, n):
    syms = sizes[n][2]
    counts = dict.fromkeys(syms, 0)
    for s in board:
        if not s == ".":
            counts[s] = counts[s] + 1
    for key in counts:
        if not counts[key] == n:
            return False
    return True


# Generate the general constraints
fileName = sys.argv[1]
#fileName = "Puzzles1.txt"
file = open(fileName)
for line in file:
    line = line.strip()
    size = int(len(line)**0.5)
    if size not in sizes.keys():
        w, h, symbols = findVals(size)
        sizes[size] = [w,h,symbols]
        constraints[size] = findCons(size)

# Generate the specific constraints
for s in constraints.keys():
    spaces = dict()
    for pos in range(int(s**2)):
        allCons = set()
        for conSet in constraints[s]:
            if pos in conSet:
                allCons = allCons | conSet
        allCons.remove(pos)                            # REMOVE
        spaces[pos] = allCons
    spaceCons[s] = spaces

# Solving
file = open(fileName)
pos = 1
for line in file:
    line = line.strip()
    size = int(len(line)**0.5)
    #print("Line " + str(pos) + ": " + str(solve(line, size)))
    print(solve(line, size))
    pos = pos + 1

# Python Sudoku1.py Puzzles1.txt
