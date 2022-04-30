# Jason Xu
# NQueens

import random

size = 10


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
    return None

def getVal(state, pos):
    vals = list()
    yVals = list()
    coords = list()
    for yVal in range(0,size):
        if yVal in state:
            yVals.append(yVal)
            coords.append((yVal,state.index(yVal)))

    for i in range(size):
        if len(yVals) > 0:
            if i not in yVals:
                works = True
                for x,y in coords:
                    xDif = abs(x-i)
                    yDif = abs(y-pos)
                    if xDif == yDif:
                        works = False
                    if (x+y) == (i+pos):
                        works = False
                if works:
                    vals.append(i)
        else:
            vals.append(i)
    return vals

def solve():
    b=list()
    for i in range(size):
        b.append(None)
    return solve1(b)

def solve1(state):
    solved = True
    for x in range(0,size):
        if state[x] == None:
            solved = False
    if solved:
        return state
    pos = getNext(state)
    for val in getVal(state,pos):
        newState = state.copy()
        newState[pos] = val
        result = solve1(newState)
        if not result == None:
            return result
    return None



print(solve())
