# Jason Xu
# NQueens Part 3

import random, time


size = 1500


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

def create():
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


def solve():
    b = create()
    colls, yvals, sums, diffs = collisions(b)
    while not 0 in colls.keys() or len(colls[0]) != size:
        numColls = 0
        for pos in colls.keys():
            numColls = numColls + (pos*len(colls[pos]))
        print("Collisions: " + str(numColls))
        #print(b)
        #print(colls)
        b, colls, yvals, sums, diffs = solver(b, colls, yvals, sums, diffs)
    return b

def solver(board,colls, yvals, sums, diffs):
    templist = list(colls.keys())
    maxPos = random.randint(0,len(templist)-1)
    maxVal = templist[maxPos]
    #maxVal = max(colls.keys())s
    vals = colls.pop(maxVal)
    random.shuffle(vals)
    index = vals.pop()
    if len(vals) > 0:
        colls[maxVal] = vals
    newval, newcolls = findMin(board, yvals, sums, diffs, index)
    #print(newcolls)
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


startTime = time.perf_counter()
solution = solve()
endTime = time.perf_counter()
print(solution)
print("Time: " + str(endTime - startTime) + " seconds")
print(test_solution(solution))