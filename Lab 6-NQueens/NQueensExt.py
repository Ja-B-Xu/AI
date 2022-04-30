#Jason Xu
#NQueens Extension - Optimization


import random, time


def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if state[compare] == left >= 0:
                print(var, "left", compare)
                return False
            if state[compare] == right < len(state):
                print(var, "right", compare)
                return False
    return True

def getNext(state):
    for val in range(len(state)):
        if state[val] is None:
            return val

def getVal(state, pos,size):
    vals = list()
    yVals = list()
    sums = set()
    diffs = set()
    for yVal in range(0,size):
        if yVal in state:
            yVals.append(yVal)
            sums.add(yVal + state.index(yVal))
            diffs.add(yVal-state.index(yVal))
    for i in range(size):
        if len(yVals) > 0:
            if i not in yVals:
                works = True
                if i-pos in diffs:
                    works = False
                if (i+pos) in sums:
                    works = False
                if works:
                    vals.append(i)
        else:
            vals.append(i)
    random.shuffle(vals)
    return vals

def bck(size):
    b=list()
    for i in range(size):
        b.append(None)
    return solve1(b,time.perf_counter(),size)

def solve1(state,t,size):
    solved = True
    newTime = time.perf_counter()
    if newTime-t > 0.5:
        return bck(size)
    if None in state:
        solved = False
    if solved:
        return state
    pos = getNext(state)
    possibles = getVal(state, pos,size)
    for val in possibles:
        newState = list(state)
        newState[pos] = val
        result = solve1(newState,t,size)
        if not result == None:
            return result
    return None

def create(size):
    nums = list()
    for i in range(size):
        nums.append(i)
    random.shuffle(nums)
    return nums

def collisions(board):
    vals = dict()
    yvals = dict()
    sums = dict()
    diffs = dict()
    for pos in range(len(board)):
        sum = pos + board[pos]
        diff = pos - board[pos]
        if sum in sums.keys():
            sums[sum] = sums[sum] + 1
        else:
            sums[sum] = 0
        if diff in diffs.keys():
                diffs[diff] = diffs[diff] + 1
        else:
            diffs[diff] = 0
        if board[pos] in yvals.keys():
            yvals[board[pos]] = yvals[board[pos]] + 1
        else:
            yvals[board[pos]] = 0
    for pos in range(len(board)):
        sum = pos + board[pos]
        diff = pos - board[pos]
        count = sums[sum] + diffs[diff] + yvals[board[pos]]
        if count in vals:
            vals[count].append(pos)
        else:
            vals[count] = [pos,]
    return vals, yvals, sums, diffs

def findMin(board, yvals, sums, diffs, pos):
    collisions = sums[pos + board[pos]] + diffs[pos - board[pos]] + yvals[board[pos]]
    mins = [board[pos]]
    for xval in range(len(board)):
        if (pos+xval) in sums.keys():
            val1 = sums[pos + xval] + 1
        else:
            val1 = 0
        if (pos - xval) in diffs.keys():
            val2 = diffs[pos - xval] + 1
        else:
            val2 = 0
        if xval in yvals.keys():
            if xval == board[pos]:
                val3 = yvals[xval]
            else:
                val3 = yvals[xval] + 1
        else:
            val3 = 0
        temp = val1 + val2 + val3
        if temp < collisions:
            del mins[:]
            mins.append(xval)
            collisions = temp
        if temp == collisions:
            mins.append(xval)
    random.shuffle(mins)
    minval = mins[0]
    return minval, collisions


def inc(size, sTime):
    b = create(size)
    colls, yvals, sums, diffs = collisions(b)
    while not 0 in colls.keys() or len(colls[0]) != size:
        if time.perf_counter() - sTime > 0.5:
            b = create(size)
            colls, yvals, sums, diffs = collisions(b)
            sTime = time.perf_counter()
        numColls = 0
        for pos in colls.keys():
            numColls = numColls + (pos*len(colls[pos]))
        #print("Collisions: " + str(numColls))
        b, colls, yvals, sums, diffs = solver(b, colls, yvals, sums, diffs)
    return b

def solver(board,colls, yvals, sums, diffs):
    templist = list(colls.keys())
    maxPos = random.randint(0,len(templist)-1)
    maxVal = templist[maxPos]
    vals = colls.pop(maxVal)
    random.shuffle(vals)
    index = vals.pop()
    if len(vals) > 0:
        colls[maxVal] = vals
    newval, newcolls = findMin(board, yvals, sums, diffs, index)
    newboard = list(board)
    newboard[index] = newval
    if newcolls in colls.keys():
        colls[newcolls].append(index)
    else:
        colls[newcolls] = [index,]
    yvals[board[index]] = yvals[board[index]] - 1
    yvals[newval] = yvals[newval] + 1
    if sums[index + board[index]] == 0:
        sums.pop(index + board[index])
    else:
        sums[index + board[index]] = sums[index + board[index]] - 1
    if (newval + index) in sums.keys():
        sums[newval + index] = sums[newval + index] + 1
    else:
        sums[newval + index] = 0
    if (index - newval) in diffs.keys():
        diffs[index - newval] = diffs[index - newval] + diffs[index - board[index]] + 1
    else:
        diffs[index - newval] = 0
    if diffs[index - board[index]] == 0:
        diffs.pop(index - board[index])
    else:
        diffs[index - board[index]] = diffs[index - board[index]] - 1

    return newboard, colls, yvals, sums, diffs


#main
solutions = []
currentSize = 8
while time.perf_counter() < 30:
    start = time.perf_counter()
    if currentSize < 55:
        solution = bck(currentSize)
    else:
        solution = inc(currentSize, start)
    end = time.perf_counter()
    print("Board size: " + str(currentSize) + " in " + str(end - start) + "seconds, total of " + str(end) + " seconds")
    solutions.append(solution)
    currentSize = currentSize + 1
for checking in range(len(solutions)):
    print("Size : " + str(checking) + " || check : " + str(test_solution(solutions[checking])))

