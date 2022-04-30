# Jason Xu
# Crosswords part 1: Dumb placement of blocking squares

import sys


# General notes:
# To move up/down, add or subtract the width
# Left edge, pos%width = 0
# Right edge, pos+1%width = 0

########################################################################################################################
# Part 0
# Reading input + generating board with no blocks
########################################################################################################################

# Generates an empty board
# Parameters: y = column height, x = row length
def generateEmpty(y,x):
    board = ""
    for i in range(y*x):
        board = board + "-"
    return board


# Places any seedstrings on the board
# Arguments: board = the board, seeds = list of seeds, width = num columns(row width)
def placeSeeds(board, seeds, width):
    boardstr = list(board)
    for seed in seeds:
        splitpos = seed.find("x")                                                                                     #Extract info from seed
        temp1 = seed[0:splitpos]
        temp2 = seed[splitpos + 1:]
        tempstr2 = ""
        word = ""
        for i in temp2:
            if i.isdigit():
                tempstr2 += i
            else:
                word += i
        ystart, xstart = int(temp1[1:]), int(tempstr2)
        startpos = ystart * width + xstart
        if seed[0].upper() == "V":
            for let in word:
                boardstr[startpos] = let.upper()
                startpos += width
        elif seed[0].upper() == "H":
            for let in word:
                boardstr[startpos] = let.upper()
                startpos += 1
        else:
            print("Seed error")
    return "".join(boardstr)


########################################################################################################################
# Part 1
# Placing blocks - dumb
########################################################################################################################

# Return a list of all blocks implied by the current board
# Arguments: board = the board, newpos = the position checked, width = width of board
def getImplied(board, newpos, width):
    implieds = set()
    up = 0
    down = 0
    if (newpos - width) >= 0 and board[newpos - width] != "#":                                                          #Up
        if (newpos - width - width) < 0 or board[newpos - width - width] == "#":
            implieds.add(newpos - width)
            up = 1
        elif (newpos - width - width - width) < 0 or board[newpos - width - width - width] == "#":
            implieds.add(newpos - width)
            implieds.add(newpos - width - width)
            up = 2
    if (newpos + width) < len(board) and board[newpos + width] != "#":                                                  #Down
        if (newpos + width + width) >= len(board) or board[newpos + width + width] == "#":
            implieds.add(newpos + width)
            down = 1
        elif (newpos + width + width + width) >= len(board) or board[newpos + width + width + width] == "#":
            implieds.add(newpos + width)
            implieds.add(newpos + width + width)
            down = 2
    if (newpos % width) > 0 and board[newpos - 1] != "#":                                                               #Left
        if ((newpos - 1) % width) == 0 or board[newpos - 2] == "#":
            implieds.add(newpos - 1)
            if up == 1:
                implieds.add(newpos - 1 - width)
            if up == 2:
                implieds.add(newpos - 1 - width)
                implieds.add(newpos - 1 - width - width)
            if down == 1:
                implieds.add(newpos - 1 + width)
            if down == 2:
                implieds.add(newpos - 1 + width)
                implieds.add(newpos - 1 + width + width)
        elif ((newpos - 2) % width) == 0 or board[newpos - 3] == "#":
            implieds.add(newpos - 1)
            implieds.add(newpos - 2)
            if up == 1:
                implieds.add(newpos - 1 - width)
                implieds.add(newpos - 2 - width)
            if up == 2:
                implieds.add(newpos - 1 - width)
                implieds.add(newpos - 2 - width)
                implieds.add(newpos - 1 - width - width)
                implieds.add(newpos - 2 - width - width)
            if down == 1:
                implieds.add(newpos - 1 + width)
                implieds.add(newpos - 2 + width)
            if down == 2:
                implieds.add(newpos - 1 + width)
                implieds.add(newpos - 2 + width)
                implieds.add(newpos - 1 + width + width)
                implieds.add(newpos - 2 + width + width)
    if ((newpos + 1) % width) > 0 and board[newpos + 1] != "#":                                                         #Right
        if ((newpos + 2) % width) == 0 or board[newpos + 2] == "#":
            implieds.add(newpos + 1)
            if up == 1:
                implieds.add(newpos + 1 - width)
            if up == 2:
                implieds.add(newpos + 1 - width)
                implieds.add(newpos + 1 - width - width)
            if down == 1:
                implieds.add(newpos + 1 + width)
            if down == 2:
                implieds.add(newpos + 1 + width)
                implieds.add(newpos + 1 + width + width)
        elif ((newpos + 3) % width) == 0 or board[newpos + 3] == "#":
            implieds.add(newpos + 1)
            implieds.add(newpos + 2)
            if up == 1:
                implieds.add(newpos + 1 - width)
                implieds.add(newpos + 2 - width)
            if up == 2:
                implieds.add(newpos + 1 - width)
                implieds.add(newpos + 2 - width)
                implieds.add(newpos + 1 - width - width)
                implieds.add(newpos + 2 - width - width)
            if down == 1:
                implieds.add(newpos + 1 + width)
                implieds.add(newpos + 2 + width)
            if down == 2:
                implieds.add(newpos + 1 + width)
                implieds.add(newpos + 2 + width)
                implieds.add(newpos + 1 + width + width)
                implieds.add(newpos + 2 + width + width)
    for i in implieds:
        if board[i] != "-":
            return None
    return implieds



# Uses floodfill to check if all spaces are connected
#
def checkConnected(board, width):
    startPos = -1
    count = 0
    for i in range(len(board)):
        if board[i] != "#":
            startPos = i
            count = count + 1
    if startPos == -1:
        return True
    bList = list(board)
    return (checkHelper(bList, startPos, width) == count)


# Recursive helper fore checkConnected
# Has some useless lines for debugging
def checkHelper(bList, start, width):
    result = 1
    bList[start] = "#"
    up, down, left, right = True, True, True, True
    if (start - width) < 0 or bList[start - width] == "#":
        up = False
    else:
        result = result + checkHelper(bList, start - width, width)
    if (start + width) >= len(bList) or bList[start + width] == "#":
        down = False
    else:
        result = result + checkHelper(bList, start + width, width)
    if start % width == 0 or bList[start - 1] == "#":
        left = False
    else:
        result = result + checkHelper(bList, start - 1, width)
    if (start + 1) % width == 0 or bList[start + 1] == "#":
        right = False
    else:
        result = result + checkHelper(bList, start + 1, width)
    return result

# Takes the current board state and mirrors the blocks
#
def mirrorCurrent(board, width):
    bList = list(board)
    blocks = []
    for i in range(len(board)):
        if board[i] == "#":
            bList[-i-1] = "#"
            blocks.append(i)
            blocks.append(len(board)-i-1)
    imps = []
    board = "".join(bList)
    for space in blocks:
        imps = getImplied(board, space, width) | getImplied(board, len(board) - space - 1, width)
        newimps = moreImps(board, width, imps)
        while imps != newimps:
            imps = newimps
            newimps = moreImps(board, width, imps)
        for i in imps:
            bList[i] = "#"
        board = "".join(bList)
    return "".join(bList)


# Find all possible options for the next square, not checking for implieds
#
def getNextBlock(board):
    nexts = []
    for i in range(len(board)//2):
        if board[i] == "-" and board[-i -1] == "-":
            nexts.append(i)
    return nexts


# Takes the original "implieds" set and find all the spaces implied by that
# Arguments: board = board, width = width, implied = starting set of implied spaces
def moreImps(board, width, implied):
    for i in implied:
        temp = getImplied(board, i, width)
        if temp is None:
            return None
        implied = implied | temp
    return implied


# Places blocking spaces
# Arguments: board = board, num = required # of blocks
def placeB(board, num, width):
    bList = list(board)
    if num%2 == 1:
        bList[len(bList)//2] = "#"
    board = "".join(bList)
    currentCount = board.count("#")
    if currentCount == num:
        if checkConnected(board, width):
            return board
    if currentCount > num:
        return None
    nexts = getNextBlock(board)
    for space in nexts:
        works = True
        bList = list(board)
        bList[space] = "#"
        bList[len(board) - space - 1] = "#"
        imps1 = getImplied(board, space, width)
        imps2 = getImplied(board, len(board) - space - 1, width)
        if imps1 is not None and imps2 is not None:
            imps = getImplied(board, space, width) | getImplied(board, len(board) - space - 1, width)
            newimps = moreImps(board, width, imps)
            while imps != newimps:                                                                                          #Repeats finding implieds until there's no change
                imps = newimps
                if imps is None:
                    works = False
                    break
                newimps = moreImps(board, width, imps)
            if works:
                for imp in imps:                                                                                                #Be faster if did it during getting imps
                    if bList[imp].isalpha():
                        works = False
                        break
                    bList[imp] = "#"
            if not checkConnected(board, width):
                works = False
            if works:
                result = placeB("".join(bList), num, width)
                if not result is None:
                    return result
    return None




########################################################################################################################
# Testing/debugging
# Also main I guess
########################################################################################################################


# Displays the board for readbility
# Arguments: board = the board, y = column height, x = row length
def display(board, y, x):
    pos = 0
    for i in range(y):
        line = ""
        for i in range(x):
            line = line + board[pos] + " "                                                                              #Adds spaces for readability
            pos += 1
        print(line)


sysinput = sys.argv

size = sysinput[1]
numblocks = int(sysinput[2])
filename = sysinput[3]
seedstrings = []
if len(sysinput) > 4:                                                                                                   #Handles seedstrings
    for i in range(4, len(sysinput)):
        seedstrings.append(sysinput[i])

ysize, xsize = int(size.split("x")[0]), int(size.split("x")[1])                                                         #ysize is height, xsize is width
board = generateEmpty(ysize, xsize)
#display(board, ysize, xsize)
print()
board = placeSeeds(board, seedstrings, xsize)
board = mirrorCurrent(board, xsize)
#print(board)
#display(board,ysize,xsize)

display(placeB(board, numblocks, xsize),ysize, xsize)



#Crosswords1.py 13x13 29 wordlist.txt
#Crosswords1.py 13x13 27 xwords.txt "H6x4no#on" "v5x5nor" "v0x0pigeon" "h0x4Trot" "H0x9fall" "V0x12limp"
