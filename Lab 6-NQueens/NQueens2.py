# Jason Xu
# NQueens Part 2

import random, time


size = 101


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

def getVal(state, pos):
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

def solve():
    b=list()
    print("Fail")
    for i in range(size):
        b.append(None)
    return solve1(b,time.perf_counter())

def solve1(state,t):
    solved = True
    newTime = time.perf_counter()
    if newTime-t > 0.5:
        return solve()
    if None in state:
        solved = False
    if solved:
        return state
    pos = getNext(state)
    possibles = getVal(state, pos)
    for val in possibles:
        newState = list(state)
        newState[pos] = val
        result = solve1(newState,t)
        if not result == None:
            return result
    return None


start = time.perf_counter()
solution=solve()
end = time.perf_counter()
print(solution)
print("Time: "+str(end-start))
print(test_solution(solution))
