#Jason Xu
#Modeling Challenge - Calibron 12


import sys


def checkArea(pHeight, pWidth, rects):
    boardArea = pHeight*pWidth
    areaSum = 0
    for r in rects:
        areaSum = areaSum + (r[0] * r[1])
    return boardArea == areaSum


def createLists(rects):
    dim1 = list()
    dim2 = list()
    rep = list()
    areas = list()
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    aIndex = 0
    for dims in rects:
        rep.append(alpha[aIndex])
        dim1.append(dims[0])
        dim2.append(dims[1])
        areas.append(dims[0] * dims[1])
        aIndex += 1
    return [rep, dim1, dim2, areas]


def findSpace(board, index, width): #Returns space left in the row
    rowNum = index // width
    endPos = width * (rowNum + 1)
    spaces = 0
    for pos in range(index, endPos):
        if board[pos] == ".":
            spaces += 1
        else:
            return spaces
    return spaces


def findPoss(rects, empty):
    poss = list()
    for dim1 in range(len(rects[1])):
        if rects[1][dim1] <= empty:
            poss.append(((1000 - rects[1][dim1] - rects[2][dim1]), dim1, 1))
    for dim2 in range(len(rects[2])):
        if rects[2][dim2] <= empty:
            poss.append(((1000 - rects[1][dim2] - rects[2][dim2]), dim2, 2))
    poss.sort()
    return poss


def posToCoords(pos, width):
    x = pos % width
    y = pos // width
    return y, x


def insert(board, bHeight, bWidth, row, column, height, width, symbol):
    bList = list(board)
    if row + height > bHeight:
        return None
    for x in range(column, column + width):
        for y in range(row, row + height):
            pos = (x + (y * bWidth))
            # print(row)
            # print(height)
            # print(bWidth)
            # print(pos)
            if bList[pos] != ".":
                return None
            bList[pos] = symbol
    board = "".join(bList)
    return board


def display(board, height, width):
    num = 0
    for i in range(height):
        print(board[num:(num + width)])
        num += width
    print()


def solve(board, rects, width, height, sols):
    if "." not in board:
        return sols
    nextSpace = board.index(".")
    empty = findSpace(board, nextSpace, width)
    possibles = findPoss(rects, empty)
    for new in possibles:
        orientation = new[2]
        newRect = new[1]
        coords = posToCoords(nextSpace, width)
        if orientation == 1:
            newBoard = insert(board, height, width, coords[0], coords[1], rects[2][newRect], rects[1][newRect],  rects[0][newRect])
        else:
            newBoard = insert(board, height, width, coords[0], coords[1], rects[1][newRect], rects[2][newRect], rects[0][newRect])
        if newBoard is not None:
            nSols = list(sols)
            if orientation == 1:
                nSols.append([str(coords[0]), str(coords[1]), str(rects[2][newRect]), str(rects[1][newRect])])
            else:
                nSols.append([str(coords[0]), str(coords[1]), str(rects[1][newRect]), str(rects[2][newRect])])
            emptyPos = newBoard.find(".")
            if emptyPos == -1:
                return nSols
            newSyms = list(rects[0])
            del newSyms[newRect]
            newDim1 = list(rects[1])
            del newDim1[newRect]
            newDim2 = list(rects[2])
            del newDim2[newRect]
            newArea = list(rects[3])
            del newArea[newRect]
            newEmpty = findSpace(newBoard, emptyPos, width)
            min1 = min(newDim1)
            min2 = min(newDim2)
            if newEmpty >=min1 or newEmpty>=min2:
                newRects = [newSyms, newDim1, newDim2, newArea]
                newSol = solve(newBoard, newRects, width, height, nSols)
                if not newSol is None:
                    return newSol

    return None


puzzle = sys.argv[1].split()
puzzle_height = int(puzzle[0])
puzzle_width = int(puzzle[1])
board = "." * puzzle_width * puzzle_height
rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]
if checkArea(puzzle_height, puzzle_width, rectangles):
    rects = createLists(rectangles)
    solution = solve(board, rects, puzzle_width, puzzle_height, list())
    if solution is None:
        print("No Solution.")
    else:
        for rect in solution:
            print(" ".join(rect))
else:
    print("Containing rectangle incorrectly sized.")
    #display(solution, puzzle_height, puzzle_width)


#Python Calibron.py "18 9 3x11 5x7 4x8 6x10 1x2"
#Python Calibron.py "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
