# Jason Xu
# Sudoku Part 1

import sys, random, time

sys.setrecursionlimit(9999)
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


def findNext(poss):
    minVal = 1000
    minPos = list()
    for index in range(len(poss)):
        if 1 < len(poss[index]) < minVal:
            minVal = len(poss[index])
            minPos = list()
            minPos.append(index)
        if len(poss[index]) == minVal:
            minPos.append(index)
    random.shuffle(minPos)
    return minPos[0]



def getVals(board, index, n):
    possibles = set(sizes[n][2])
    cons = spaceCons[n][index]
    for val in cons:
        if board[val] in possibles:
            possibles.remove(board[val])
    return possibles


def genPoss(board, n):
    indexPoss = list()
    for x in range(len(board)):
        if not board[x] == ".":
            indexPoss.append(str(board[x]))
        else:
            vals = getVals(board, x, n)
            strVals = "".join(vals)
            indexPoss.append(strVals.strip())
    return indexPoss


def newPoss(poss, n, index, val):
    neighbors = spaceCons[n][index]
    for connected in neighbors:
        connectedPoss = list(poss[connected])
        if val in connectedPoss:
            connectedPoss.remove(val)
            if len(connectedPoss) == 0:
                return None
            poss[connected] = "".join(connectedPoss).strip()
    return poss


def conProp(board, n, poss):
    cons = constraints[n]
    vals = sizes[n][2]
    bList = list(board)
    prev = "".join(poss)
    next = ""
    while prev != next:
        for consSet in cons:
            do = False
            curVals = set()
            for index in consSet:
                if bList[index] == ".":
                    do = True
                else:
                    curVals.add(bList[index])
            if do:
                for val in vals:
                    if not val in curVals:
                        possSpaces = list()
                        for index in consSet:
                            possVals = list(poss[index])
                            if val in possVals:
                                possSpaces.append(index)
                        if len(possSpaces) == 1:
                            bList[possSpaces[0]] = val
                            poss = newPoss(poss, n, possSpaces[0], val)
                            if poss is None:
                                return None
                        if len(possSpaces) == 0:
                            return None
        prev = next
        next = "".join(poss)
    board = "".join(bList).strip()
    return board,poss



def lookForward(board, poss, n):
    prev = "".join(poss)
    next = ""
    bList = list(board)
    while prev != next:
        for x in range(len(poss)):
            if len(poss[x]) == 1 and bList[x] == ".":
                bList[x] = poss[x]
                poss = newPoss(poss, n, x, poss[x])
                if poss is None:
                    return None
            if len(poss[x]) == 0:
                return None
        prev = next
        next = "".join(poss)
    board = "".join(bList).strip()
    return board,poss

def solve(board, poss, n):
    if check(board):
        return board
    conCheck = conProp(board, n, poss)
    if conCheck is None:
        return None
    board, poss = conCheck
    nextPos = findNext(poss)
    nextVals = getVals(board, nextPos, n)
    for val in nextVals:
        boardList = list(board)
        boardList[nextPos] = val
        board = "".join(boardList)
        poss = genPoss(board,n)
        solutionlist = lookForward(board, poss, n)
        if not solutionlist is None:
            board2, poss2 = solutionlist
            result = solve(board2, poss2, n)
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
#fileName = sys.argv[1]
fileName = "TestPuzzles.txt"
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
        allCons.remove(pos)
        spaces[pos] = allCons
    spaceCons[s] = spaces

# Solving
file = open(fileName)
pos = 1
start = time.perf_counter()
for line in file:
    line = line.strip()
    size = int(len(line)**0.5)
    poss = genPoss(line, size)
    first, first2 = lookForward(line,poss,size)
    if check(first):
        print("Line " + str(pos) + ": " + str(first) + " just FL")
    else:
        print("Line " + str(pos) + ": " + str(solve(first, first2, size)))
        #print(solve(line, poss, size))
    pos = pos + 1
end = time.perf_counter()
print("Time: " + str(end-start))
# Python SudokuTest.py Puzzles1.txt
