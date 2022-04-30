#Jason Xu
#Othello Testing

import random


# ??????????
# ?........?
# ?........?
# ?........?
# ?...o@...?
# ?...@o...?
# ?........?
# ?........?
# ?........?
# ??????????
#
# ???????????........??........??........??...o@...??...@o...??........??........??........???????????

initialBoard = "???????????........??........??........??...o@...??...@o...??........??........??........???????????"



def checkSquare(board,square,token): #Check a square for all possible moves, returns dict with possible move as key and associated(turned) squares as vals
    possibles = set()
    left = square - 1
    right = square + 1
    up = square - 10
    down = square + 10
    UL = square - 11
    UR = square - 9
    DL = square + 9
    DR = square + 11
    for x in range(9):

        if board[left] == token:
            left -= 1
        elif left != (square - 1):
            if board[left] == ".":
                possibles.add(left)

        if board[right] == token:
            right += 1
        elif right != (square + 1):
            if board[right] == ".":
                possibles.add(right)

        if board[up] == token:
            up -= 10
        elif up != (square - 10):
            if board[up] == ".":
                possibles.add(up)

        if board[down] == token:
            down += 10
        elif down != (square + 10):
            if board[down] == ".":
                possibles.add(down)

        if board[UL] == token:
            UL -= 11
        elif UL != (square - 11):
            if board[UL] == ".":
                possibles.add(UL)

        if board[UR] == token:
            UR -= 9
        elif UR != (square - 9):
            if board[UR] == ".":
                possibles.add(UR)

        if board[DL] == token:
            DL += 9
        elif DL != (square + 9):
            if board[DL] == ".":
                possibles.add(DL)

        if board[DR] == token:
            DR += 11
        elif DR != (square + 11):
            if board[DR] == ".":
                possibles.add(DR)
    return possibles


def checkMids(board, square, token, other):  # Check a square in all directions, return a set of each associated(turned) square
    associated = set()
    left = square - 1
    leftSet = set()
    right = square + 1
    rightSet = set()
    up = square - 10
    upSet = set()
    down = square + 10
    downSet = set()
    UL = square - 11
    ULSet = set()
    UR = square - 9
    URSet = set()
    DL = square + 9
    DLSet = set()
    DR = square + 11
    DRSet = set()
    for x in range(9):

        if board[left] == other:
            leftSet.add(left)
            left -= 1
        elif left != (square - 1):
            if board[left] == token:
                associated = associated | leftSet

        if board[right] == other:
            rightSet.add(right)
            right += 1
        elif right != (square + 1):
            if board[right] == token:
                associated = associated | rightSet

        if board[up] == other:
            upSet.add(up)
            up -= 10
        elif up != (square - 10):
            if board[up] == token:
                associated = associated | upSet

        if board[down] == other:
            downSet.add(down)
            down += 10
        elif down != (square + 10):
            if board[down] == token:
                associated = associated | downSet

        if board[UL] == other:
            ULSet.add(UL)
            UL -= 11
        elif UL != (square - 11):
            if board[UL] == token:
                associated = associated | ULSet

        if board[UR] == other:
            URSet.add(UR)
            UR -= 9
        elif UR != (square - 9):
            if board[UR] == token:
                associated = associated | URSet

        if board[DL] == other:
            DLSet.add(DL)
            DL += 9
        elif DL != (square + 9):
            if board[DL] == token:
                associated = associated | DLSet

        if board[DR] == other:
            DRSet.add(DR)
            DR += 11
        elif DR != (square + 11):
            if board[DR] == token:
                associated = associated | DRSet
    return associated

def possibleMoves(board, token):
    if token == "@":
        other = "o"
    else:
        other = "@"
    currents = list()
    possibles = set()
    for pos in range(len(board)):
        if board[pos] == token:
            currents.append(pos)
    for square in currents:
        possibles = possibles | checkSquare(board, square, other)
    return possibles

def move(board, space, token, other):
    if board[space] != ".":
        return "Something broke"
    bList = list(board)
    newSpaces = checkMids(board, space, token, other)
    for pos in newSpaces:
        bList[pos] = token
    bList[space] = token
    return "".join(bList)


def bMove(board,moveList):
    display(board)
    if "." not in board:
        print("Final scores: ")
        printScores(board)
        print(moveList)
        return board, moveList
    printScores(board)
    possibles = possibleMoves(board, "@")
    pList = list(possibles)
    if not pList:
        print("No valid moves")
        print("Pass\n")
        moveList.append(-1)
        return wMove(board, moveList)
    else:
        pList.sort()
        print(pList)
        random.shuffle(pList)
        board = move(board, pList[0], "@", "o")
        print("Black moved at space " + str(pList[0]))
        print()
        moveList.append(pList[0])
        return wMove(board, moveList)

def wMove(board,moveList):
    display(board)
    if "." not in board:
        print("Final scores: ")
        printScores(board)
        print(moveList)
        return board, moveList
    printScores(board)
    possibles = possibleMoves(board, "o")
    pList = list(possibles)
    if not pList:
        print("No valid moves")
        print("Pass\n")
        moveList.append(-1)
        return bMove(board, moveList)
    else:
        pList.sort()
        print(pList)
        random.shuffle(pList)
        board = move(board, pList[0], "o", "@")
        print("White moved at space " + str(pList[0]))
        print()
        moveList.append(pList[0])
        return bMove(board, moveList)


def printScores(board):
    bCount = 0
    wCount = 0
    for ch in board:
        if ch == "@":
            bCount += 1
        if ch == "o":
            wCount += 1
    print("Black: " + str(bCount) + "\tWhite: " + str(wCount))


def display(board):
    x = 0
    for y in range(10):
        print(board[x:x+10])
        x += 10


initialMoves = list()
bMove(initialBoard, initialMoves)
