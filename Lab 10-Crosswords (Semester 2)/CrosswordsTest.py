# Jason Xu
# Crosswords part 3: Smart placement of blocking squares

import sys
import random

sys.setrecursionlimit(99999999)

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
        if board[i] != "-" and board[i] != "#":
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
    currentcount = board.count("#")
    if currentcount == num:
        if checkConnected(board, width):
            return board
    if currentcount > num:
        return None
    nexts = getNextBlock(board)
    possiblemoves = []
    for space in nexts:
        works = True
        bList = list(board)
        bList[space] = "#"
        bList[len(board) - space - 1] = "#"
        imps1 = getImplied(board, space, width)
        imps2 = getImplied(board, len(board) - space - 1, width)
        if imps1 is not None and imps2 is not None:
            imps = imps1 | imps2
            newimps = moreImps(board, width, imps)
            while imps != newimps:                                                                                      #Repeats finding implieds until there's no change
                imps = newimps
                if imps is None:
                    works = False
                    break
                newimps = moreImps(board, width, imps)
            if works:
                for imp in imps:                                                                                        #Be faster if did it during getting imps
                    if bList[imp].isalpha():
                        works = False
                        break
                    bList[imp] = "#"
            if not checkConnected(board, width):
                works = False
            if works:
                possiblemoves.append("".join(bList))
    possiblemoves = sortMoves(possiblemoves, width, currentcount)
    for move in possiblemoves:
        result = placeB(move, num, width)
        if result is not None:
            return result
    return None


########################################################################################################################
# Part 3
# Smart blocking
########################################################################################################################


def sortMoves(possibles, width, previouscount):
    numwords = []
    for poss in range(len(possibles)):
        numwords.append(blockHeuristic(possibles[poss], width, previouscount))
    newpossibles = [x for _,x in sorted(zip(numwords, possibles))]
    return newpossibles

# Heuristic based on word lengths, longer word lengths create bigger values which are sorted last
#
def blockHeuristic(board, width, previouscount):
    newnum = board.count("#") - previouscount
    possplaces = possiblePlacesIncl(board, width)
    score = len(possplaces) * 100000
    if score == 0:
        return 99999999999
    for i in possplaces:
        if len(i) > 3:
            score -= ((len(i) - 3) ** 2)
    return (newnum * 10000) / score


#Same as possible places but includes full words with no blanks
#
def possiblePlacesIncl(board, width):
    possibles = []
    processedhoriz = set()
    processedvert = set()
    for pos in range(len(board)):
        if board[pos] != "#":
            if pos not in processedhoriz:                                                                               #Processes horizontal words
                wordpositions = []
                temppos = pos + 1
                wordpositions.append(pos)
                while (temppos)%width != 0 and board[temppos] != "#":
                    wordpositions.append(temppos)
                    processedhoriz.add(temppos)
                    temppos += 1
                possibles.append(wordpositions)
            if pos not in processedvert:
                wordpositions = []
                temppos = pos + width
                wordpositions.append(pos)
                while (temppos) < len(board) and board[temppos] != "#":
                    wordpositions.append(temppos)
                    processedvert.add(temppos)
                    temppos += width
                possibles.append(wordpositions)
    return possibles
########################################################################################################################
# Part 2
# By word - do full bucketing up to a point - maybe max 7 letters, above 7 just do during runtime
########################################################################################################################

# Takes a word and returns all associated buckets
# Arguments: word = the word
def makeBuckets(word, current):
    bucks = set()
    blankpos = word.find("-")
    if blankpos == -1:                                                                                                  #If there are no blanks, start from front
        for pos in range(len(word)):
            if word[pos] != "-":
                temp = list(word)
                temp[pos] = "-"
                newbuck = "".join(temp)
                bucks.add(newbuck)
                if not newbuck in current:
                    bucks = bucks | makeBuckets(newbuck, bucks)
    else:                                                                                                               #If there are blanks, start at blank and go right
        for pos in range(blankpos, len(word)):
            if word[pos] != "-":
                temp = list(word)
                temp[pos] = "-"
                newbuck = "".join(temp)
                bucks.add(newbuck)
                if not newbuck in current:
                    bucks = bucks | makeBuckets(newbuck, bucks)
    return bucks


# Processes the dictionary
# Removes invalid words (<3 letters or with number), return frequency list of words and buckets of 6 + dict of 7 or more
# Freq list is dict of let:freq
# Buckets is dict of str:word, with blanks represented as "-"(dashes)
# Dict is dict of length:set of words
# Arguments: words = name of dictionary file
def processDict(filename):
    buckets = {}
    freq = {}
    dic = {}
    with open(filename) as f:
        for line in f:
            line = line.strip().upper()
            if len(line) >= 3 and line.strip().isalpha():
                for let in line:                                                                                        #Creating the frequency dict
                    if let in freq.keys():
                        freq[let] += 1
                    else:
                        freq[let] = 1
                if len(line) < 7:                                                                                       #Makes the buckets if word shorter than 7
                    if len(line) in dic.keys():
                        dic[len(line)].add(line)
                    else:
                        dic[len(line)] = {line}
                    startbucks = set()
                    newbucks = makeBuckets(line, startbucks)
                    buckets[line] = [line]
                    for newbuck in newbucks:
                        if newbuck in buckets.keys():
                            buckets[newbuck].add(line)
                        else:
                            buckets[newbuck] = {line}
                else:                                                                                                   #Only adds to dictionary if 7 or longer
                    if len(line) in dic.keys():
                        dic[len(line)].add(line)
                    else:
                        dic[len(line)] = {line}
    return freq, buckets, dic


#Returns a dict with every word(tuple) as a key and every word that a word intersects in a set of tuples
#
def getIntersects(posswords):
    inters = {}
    for w in posswords:
        w1 = set(w)
        w2 = tuple(w)
        inter = set()
        for x in posswords:
            x1 = set(x)
            x2 = tuple(x)
            temp = w1.intersection(x1)
            if len(temp) == 1:
                inter.add(x2)
        inters[w2] = inter
    return inters


# Returns the value of a word. Higher is better
# Arguments: word = the word, freqs = frequency list of all letters
def wordVal(word, freqs):
    val = 0
    for let in word:
        val += freqs[let]
    return val


# Returns a list of possible positions to place new words(represented as a list of indeces)
# Arguments: board = the board
def possiblePlaces(board, width):
    possibles = []
    processedhoriz = set()
    processedvert = set()
    for pos in range(len(board)):
        if board[pos] != "#":
            if pos not in processedhoriz:                                                                               #Processes horizontal words
                hasblank = False
                wordpositions = []
                temppos = pos + 1
                wordpositions.append(pos)
                while (temppos)%width != 0 and board[temppos] != "#":
                    if board[temppos] == "-":
                        hasblank = True
                    wordpositions.append(temppos)
                    processedhoriz.add(temppos)
                    temppos += 1
                if hasblank:
                    possibles.append(wordpositions)
            if pos not in processedvert:
                hasblank = False
                wordpositions = []
                temppos = pos + width
                wordpositions.append(pos)
                while (temppos) < len(board) and board[temppos] != "#":
                    if board[temppos] == "-":
                        hasblank = True
                    wordpositions.append(temppos)
                    processedvert.add(temppos)
                    temppos += width
                if hasblank:
                    possibles.append(wordpositions)
    return possibles


# Returns list of all the possible words given an incomplete word
# Arguments: board = the board, spaces = list of positions, dictionary = the dict of 7+
# Need to fix: doesn't consider if the word messes with other possibilities (basically need to add"forward looking")
def getPossibleWords(board, spaces):
    word = ""
    possibles = []
    for let in spaces:
        word += board[let]
    if len(word) < 7:
        if word in buckets.keys():
            return list(buckets[word])
        else:
            return []
    elif word in buckets.keys():
        return list(buckets[word])
    for possword in dictionary[len(word)]:
        works = True
        for pos in range(len(possword)):
            if word[pos] != "-" and word[pos] != possword[pos]:
                works = False
                break
        if works:
            possibles.append(possword)
    buckets[word] = possibles
    return possibles


# def getAllPossibleWords(board, spaces):
#     poss = getPossibleWords(board, spaces)
#     for word in poss:
#         newboard = placeWords(board, spaces, word)
#         result = getAllPossibleWords(newboard)

# Returns the most constrained word(represented as a list of positions) along with its possible words
# Arguments: possibles = list of possible word positions, possiblewords = all the possible words everywhere
def mostConstrained(possibles, possiblewords):
    leastposs = 999999
    mostcons = []
    posswords = []
    for poslist in possibles:
        allposition = allpossibles.index(poslist)
        possw = possiblewords[allposition]
        count = len(possw)
        if count == 0:
            print("hehe")
            return None, None
        if count < leastposs:
            mostcons = poslist[:]
            leastposs = count
            posswords = possw[:]
    return mostcons, posswords


# Returns the best word(string) in a given blank line using frequency of letters, the higher the better
# Arguments: possibles = list of possible word strings frequencies = freq dict
def getBest(possibles, frequencies):
    maxscore = 0
    bestword = ""
    for w in possibles:
        score = 0
        for let in w:
            score += frequencies[let]
        if score > maxscore:
            bestword = w
            maxscore = score
    return bestword


def placeWords(board, positions, word):
    newboard = list(board)
    for i in range(len(positions)):
        newboard[positions[i]] = word[i]
    return "".join(newboard)


# Returns all the possible words at ALL original word positions, also checks if broken by returning none
# Arguments: board = the board

def allPossibles(board):
    possibles = []
    for wordpos in allpossibles:
        posses = getPossibleWords(board,wordpos)
        if len(posses) == 0:
            return None
        possibles.append(posses)
    return possibles

# Uses recursive backtracking to solve the puzzle, taking the most constrained space every time
#
def solve(board, width, used):
    possiblewords = allPossibles(board)
    if possiblewords is None:
        return None
    if not "-" in board:
        return board
    display(board, ysize, xsize)
    nexts = possiblePlaces(board, width)
    mostcon, possibles = mostConstrained(nexts, possiblewords)
    while possibles:
        best = getBest(possibles, frequencies)
        possibles.remove(best)
        inters = intersects[tuple(mostcon)]
        if best not in used:
            newboard = placeWords(board, mostcon, best)
            works = False
            newused = used.copy()
            newused.add(best)
            for cross in inters:                                                                                        #Checking the immediate intersections
                nextposs = getPossibleWords(newboard, list(cross))
                if len(nextposs) == 0:
                    works = False
                else:
                    for poss in nextposs:
                        if poss not in newused:
                            works = True
                            if len(nextposs) == 1:
                                newused.add(poss)
                            break
            if works:
                result = solve(newboard, width, newused)
                if result is not None:
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
        print(line.upper())
    print()


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
board = placeB(board, numblocks, xsize)
display(board,ysize, xsize)
allpossibles = possiblePlaces(board, xsize)
frequencies, buckets, dictionary = processDict(filename)
intersects = getIntersects(allpossibles)
useds = set()
display(solve(board, xsize, useds),ysize, xsize)




#Crosswords3.py 4x4 0 wordlist.txt
#Crosswords3.py 7x7 11 twentyk.txt
#Crosswords3.py 4x4 0 twentyk.txt
#Crosswords3.py 9x13 19 "twentyk.txt" "v2x3#" "v1x8#" "h3x1#" "v4x5##"