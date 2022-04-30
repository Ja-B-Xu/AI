#Jason Xu

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
#Mid-Weight matrix (0 represents like -10 or something):
# ??????????
# ?90555509?
# ?00111100?
# ?51122115?
# ?51233215?
# ?51233215?
# ?51122115?
# ?00111100?
# ?90555509?
# ??????????

# ???????????90555509??00111100??51122115??51233215??51233215??51122115??00111100??90555509???????????




import random
import sys

earlyMatrix = [0,0,0,0,0,0,0,0,0,0,0,100,-100,5,5,5,5,-100,100,0,0,-100,-100,-1,-1,-1,-1,-100,-100,0,0,5,-1,0,0,0,0,-1,5,0,0,5,-1,0,0,0,0,-1,5,0,0,5,-1,0,0,0,0,-1,5,0,0,5,-1,0,0,0,0,-1,5,0,0,-100,-100,-1,-1,-1,-1,-100,-100,0,0,100,-100,5,5,5,5,-100,100,0,0,0,0,0,0,0,0,0,0,0,]
dynamicMatrix = [0,0,0,0,0,0,0,0,0,0,0,5000,-2000,5,5,5,5,-2000,5000,0,0,-2000,-2000,-1,-1,-1,-1,-2000,-2000,0,0,5,-1,1,2,2,1,-1,5,0,0,5,-1,2,3,3,2,-1,5,0,0,5,-1,2,3,3,2,-1,5,0,0,5,-1,1,2,2,1,-1,5,0,0,-2000,-2000,-1,-1,-1,-1,-2000,-2000,0,0,5000,-2000,5,5,5,5,-2000,5000,0,0,0,0,0,0,0,0,0,0,0,]



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


def bMove(board,alpha,beta,moveNum,depth): #Min
    if depth == 0:
        if moveNum < 21:
            return earlyHB(board), -2
        elif moveNum < 55:
            return midHeuristic(board), -3
        else:
            return lateHeuristic(board), -4
    if "." not in board:
        return lateHeuristic(board), -5
    possibles = possibleMoves(board, "@")
    pList = list(possibles)
    if len(pList) == 0:
        return 1000, 998
    best = 99999999
    bestPos = -11
    for poss in pList:
        newBoard = move(board, poss, "@", "o")
        result = wMove(newBoard, alpha, beta, moveNum, depth - 1)[0]
        if result < best:
            best = result
            bestPos = poss
        if result < beta:                   #PRUNING
            beta = result
        if alpha >= beta:                   #PRUNING
            if moveNum < 21:
                return earlyHB(board), bestPos
            elif moveNum < 55:
                return midHeuristic(board), bestPos
            else:
                return lateHeuristic(board), bestPos

    return best, bestPos


def wMove(board,alpha,beta,moveNum,depth): #Max
    if depth == 0:
        if moveNum < 21:
            return earlyHW(board),-6
        elif moveNum < 55:
            return midHeuristic(board),-7
        else:
            return lateHeuristic(board),-8
    if "." not in board:
        return lateHeuristic(board),-9
    possibles = possibleMoves(board, "o")
    pList = list(possibles)
    if len(pList) == 0:
        return -1000, 999
    best = -99999999
    bestPos = -10
    for poss in pList:
        newBoard = move(board, poss, "o", "@")
        result = bMove(newBoard, alpha, beta, moveNum, depth - 1)[0]
        if result > best:
            best = result
            bestPos = poss
        if result > alpha:                  #PRUNING
            alpha = result
        if alpha >= beta:                   #PRUNING
            if moveNum < 21:
                return earlyHW(board), bestPos
            elif moveNum < 55:
                return midHeuristic(board), bestPos
            else:
                return lateHeuristic(board), bestPos
    return best, bestPos


def earlyHB(board):                                                 #CHANGES: early-game heuristic for black, focuses on mobility but also taking corners
    blackMoves = len(possibleMoves(board, "@"))
    score = 0
    for pos in range(len(board)):
        if board[pos] == "o":
            score = score + dynamicMatrix[pos]
        if board[pos] == "@":
            score = score - dynamicMatrix[pos]
    return score + (50 * blackMoves)

def earlyHW(board):                                                  #CHANGES: early-game heuristic for white, focuses on mobility but also taking corners
    whiteMoves = len(possibleMoves(board, "o"))
    score = 0
    for pos in range(len(board)):
        if board[pos] == "o":
            score = score + dynamicMatrix[pos]
        if board[pos] == "@":
            score = score - dynamicMatrix[pos]
    return score + (50 * whiteMoves)

def midHeuristic(board): #Weight matrix                               #CHANGES: mid-game heuristic, uses a dynamic weight matrix that updates
    score = 0
    for pos in range(len(board)):
        if board[pos] == "o":
            score = score + dynamicMatrix[pos]
        if board[pos] == "@":
            score = score - dynamicMatrix[pos]
    return score

def lateHeuristic(board):                                               #CHANGES: Late-game, greedy
    score = 0
    for space in board:
        if space == "o":
            score += 1
        elif space == "@":
            score -= 1
    return score

def updateMatrix(board):                                               #CHANGES: Updates dynamic weight matrix to account for edge stability in early & mid-game
    if board[11] != ".":
        dynamicMatrix[12], dynamicMatrix[21], dynamicMatrix[22] = 1000, 1000, 1000
    if board[18] != ".":
        dynamicMatrix[17], dynamicMatrix[27], dynamicMatrix[28] = 1000, 1000, 1000
    if board[81] != ".":
        dynamicMatrix[82], dynamicMatrix[71], dynamicMatrix[72] = 1000, 1000, 1000
    if board[88] != ".":
        dynamicMatrix[87], dynamicMatrix[78], dynamicMatrix[77] = 1000, 1000, 1000
    if board[12] != ".":
        dynamicMatrix[13] = 300
    if board[21] != ".":
        dynamicMatrix[31] = 300
    if board[17] != ".":
        dynamicMatrix[16] = 300
    if board[28] != ".":
        dynamicMatrix[38] = 300
    if board[82] != ".":
        dynamicMatrix[83] = 300
    if board[71] != ".":
        dynamicMatrix[61] = 300
    if board[87] != ".":
        dynamicMatrix[86] = 300
    if board[78] != ".":
        dynamicMatrix[68] = 300

class Strategy():                                               #CHANGES: Early is first 20 total moves, Mid is 21-54, Late is 55-60
    def best_strategy(self,board,player,best_move,still_running):
        updateMatrix(board)
        ct = board.count(".")
        moveNum = 60 - ct
        depth = 1
        while (ct + depth) <= 64:
            alpha, beta = -999999999, 999999999                 #PRUNING
            if player == "o":
                val = wMove(board, alpha, beta, moveNum, depth)
                best_move.value = val[1]
            else:
                val = bMove(board, alpha, beta, moveNum, depth)
                best_move.value = val[1]
            depth += 1


#Random submission:

# curBoard, player = sys.argv[1], sys.argv[2]
# updateMatrix(curBoard)
# ct = curBoard.count(".")
# moveNum = 60 - ct
# depth = 1
# while(ct + depth) <= 64:
#     alpha, beta = -999999999, 999999999
#     if player == "o":
#         val = wMove(curBoard, alpha, beta, moveNum, depth)
#         print(val[1])
#     else:
#         val = bMove(curBoard, alpha, beta, moveNum, depth)
#         print(val[1])
#     depth += 1


#Python strategy.py "???????????.@....o.??.@@..o..??.@o@o...??..@oo...??..@oo...??.@......??........??........???????????" @