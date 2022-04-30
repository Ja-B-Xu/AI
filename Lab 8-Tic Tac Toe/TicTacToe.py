#Jason Xu
#Tic Tac Toe Minimax

import sys



def check(b):
    board = list(b)
    if board[0] == "X" and board[1] == "X" and board[2] == "X":
        return 1
    if board[3] == "X" and board[4] == "X" and board[5] == "X":
        return 1
    if board[6] == "X" and board[7] == "X" and board[8] == "X":
        return 1
    if board[0] == "X" and board[3] == "X" and board[6] == "X":
        return 1
    if board[1] == "X" and board[4] == "X" and board[7] == "X":
        return 1
    if board[2] == "X" and board[5] == "X" and board[8] == "X":
        return 1
    if board[0] == "X" and board[4] == "X" and board[8] == "X":
        return 1
    if board[2] == "X" and board[4] == "X" and board[6] == "X":
        return 1

    if board[0] == "O" and board[1] == "O" and board[2] == "O":
        return -1
    if board[3] == "O" and board[4] == "O" and board[5] == "O":
        return -1
    if board[6] == "O" and board[7] == "O" and board[8] == "O":
        return -1
    if board[0] == "O" and board[3] == "O" and board[6] == "O":
        return -1
    if board[1] == "O" and board[4] == "O" and board[7] == "O":
        return -1
    if board[2] == "O" and board[5] == "O" and board[8] == "O":
        return -1
    if board[0] == "O" and board[4] == "O" and board[8] == "O":
        return -1
    if board[2] == "O" and board[4] == "O" and board[6] == "O":
        return -1

    if "." not in board:
        return 0

    return None


def newBoards(board, ch):
    newB = list()
    positions = list()
    boardList = list(board)
    for space in range(len(boardList)):
        if boardList[space] == ".":
            positions.append(space)
            newBoard = list(boardList)
            newBoard[space] = ch
            newB.append(newBoard)
    return newB, positions


def xMove(board):
    val = check(board)
    if not val is None:
        return [[val],-100]
    newBs, positions = newBoards(board,"X")
    possibles = list()
    for b in range(len(newBs)):
        result = oMove(newBs[b])[0]
        possibles.append(min(result))
    return possibles, positions


def oMove(board):
    val = check(board)
    if not val is None:
        return [[val],-100]
    newBs, positions = newBoards(board,"O")
    possibles = list()
    for b in range(len(newBs)):
        result = xMove(newBs[b])[0]
        possibles.append(max(result))
    return possibles, positions


def xStart(board):
    possibles, positions = xMove(board)
    if positions == -100:
        print("X has already won")
    else:
        while positions != -100:
            for poss in range(len(possibles)):
                if possibles[poss] == -1:
                    print("Moving at " + str(positions[poss]) + " results in a loss")
                elif possibles[poss] == 0:
                    print("Moving at " + str(positions[poss]) + " results in a tie")
                else:
                    print("Moving at " + str(positions[poss]) + " results in a win")
            print()
            best = max(possibles)
            space = possibles.index(best)
            print("I choose space " + str(positions[space]))
            print()
            bList = list(board)
            bList[positions[space]] = "X"
            board = "".join(bList)
            print("Current board:")
            printBoard(board)
            status = check(board)
            if status is not None:
                if status == 0:
                    print("We tied!")
                else:
                    print("I win!")
                return
            del positions[space]
            tempPositions = [str(s) for s in positions]
            print("You can move to any of these spaces: " + (", ".join(tempPositions)))
            playerMove = int(input("Your choice? "))
            if playerMove not in positions:
                print("That's not a valid space.")
                sys.exit(0)
            print()
            bList = list(board)
            bList[playerMove] = "O"
            board = "".join(bList)
            print("Current board:")
            printBoard(board)
            status = check(board)
            if status is not None:
                if status == 0:
                    print("We tied!")
                else:
                    print("You win!")
                return
            possibles, positions = xMove(board)

def oStart(board):
    possibles, positions = oMove(board)
    if positions == -100:
        print("O has already won")
    else:
        while positions != -100:
            tempPositions = [str(s) for s in positions]
            print("You can move to any of these spaces: " + (", ".join(tempPositions)))
            playerMove = int(input("Your choice? "))
            if playerMove not in positions:
                print("That's not a valid space.")
                sys.exit(0)
            print()
            bList = list(board)
            bList[playerMove] = "X"
            board = "".join(bList)
            print("Current board:")
            printBoard(board)
            status = check(board)
            if status is not None:
                if status == 0:
                    print("We tied!")
                else:
                    print("You win!")
                return
            possibles, positions = oMove(board)
            for poss in range(len(possibles)):
                if possibles[poss] == -1:
                    print("Moving at " + str(positions[poss]) + " results in a win")
                elif possibles[poss] == 0:
                    print("Moving at " + str(positions[poss]) + " results in a tie")
                else:
                    print("Moving at " + str(positions[poss]) + " results in a loss")
            print()
            best = min(possibles)
            space = possibles.index(best)
            print("I choose space " + str(positions[space]))
            print()
            bList = list(board)
            bList[positions[space]] = "O"
            board = "".join(bList)
            print("Current board:")
            printBoard(board)
            status = check(board)
            if status is not None:
                if status == 0:
                    print("We tied!")
                else:
                    print("I win!")
                return

def oStartMiddle(board):
    possibles, positions = oMove(board)
    if positions == -100:
        print("O has already won")
    else:
        while positions != -100:
            for poss in range(len(possibles)):
                if possibles[poss] == -1:
                    print("Moving at " + str(positions[poss]) + " results in a win")
                elif possibles[poss] == 0:
                    print("Moving at " + str(positions[poss]) + " results in a tie")
                else:
                    print("Moving at " + str(positions[poss]) + " results in a loss")
            print()
            best = min(possibles)
            space = possibles.index(best)
            print("I choose space " + str(positions[space]))
            print()
            bList = list(board)
            bList[positions[space]] = "O"
            board = "".join(bList)
            print("Current board:")
            printBoard(board)
            status = check(board)
            if status is not None:
                if status == 0:
                    print("We tied!")
                else:
                    print("I win!")
                return
            del positions[space]
            tempPositions = [str(s) for s in positions]
            print("You can move to any of these spaces: " + (", ".join(tempPositions)))
            playerMove = int(input("Your choice? "))
            if playerMove not in positions:
                print("That's not a valid space.")
                sys.exit(0)
            print()
            bList = list(board)
            bList[playerMove] = "X"
            board = "".join(bList)
            print("Current board:")
            printBoard(board)
            status = check(board)
            if status is not None:
                if status == 0:
                    print("We tied!")
                else:
                    print("You win!")
                return
            possibles, positions = oMove(board)

def printBoard(board):
    print(str(board[0:3]) + "\t012")
    print(str(board[3:6]) + "\t345")
    print(str(board[6:9]) + "\t678")
    print()


board = sys.argv[1]

if "X" in board or "O" in board:
    dotCount = 0
    for c in board:
        if c ==".":
            dotCount+=1
    print("Current board:")
    printBoard(board)
    if dotCount%2 == 1:
        xStart(board)
    else:
        oStartMiddle(board)
else:
    starting = input("Should I be X or O? ")
    starting = starting.upper()
    print()
    print("Current board:")
    printBoard(board)
    if starting == "X":
        xStart(board)
    elif starting == "O":

        oStart(board)
    else:
        print("Please choose either X or O.")

# Python TicTacToe.py "........."