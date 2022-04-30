#Jason Xu
#Sliding Puzzles Part 1

from collections import deque
import time
import sys

def printPuzzle(len,s):
    pos=0
    for line in range(0,len):
        lin=""
        for x in range(0,len):
            lin=lin+s[pos]+" "
            pos=pos+1
        print(lin)
    print("")

def findGoal(s):
    s1 = sorted(s.replace(".",""))
    s2="".join(s1)+".".strip()
    return s2.strip()

def getChildren(board,len):
    children=[]
    strPos=board.find(".")
    x,y=posToCoord(strPos,len)
    if(x>1):
        pos=coordToPos(x-1,y,len)
        bList=list(board)
        temp=bList[pos]
        bList[pos]=bList[strPos]
        bList[strPos]=temp
        children.append("".join(bList).strip())
    if(x<len):
        pos=coordToPos(x+1,y,len)
        bList=list(board)
        temp=bList[pos]
        bList[pos]=bList[strPos]
        bList[strPos]=temp
        children.append("".join(bList).strip())
    if(y>1):
        pos=coordToPos(x,y-1,len)
        bList=list(board)
        temp=bList[pos]
        bList[pos]=bList[strPos]
        bList[strPos]=temp
        children.append("".join(bList).strip())
    if(y<len):
        pos=coordToPos(x,y+1,len)
        bList=list(board)
        temp=bList[pos]
        bList[pos]=bList[strPos]
        bList[strPos]=temp
        children.append("".join(bList).strip())
    return children

def goalTest(board):
    return board==findGoal(board)

def coordToPos(x,y,len):
    return (len*(y-1))+x-1

def posToCoord(x,len):
    return x%len+1,int(x/len+1)

# *****************************************************
# Main
# *****************************************************

#Part 1-3:Modeling
#fileName=input("File name?\n")
# with open("slide_puzzle_tests.txt") as f:
#     lineNum=1
#     for line in f:
#         print("Puzzle #"+str(lineNum)+": ")
#         printPuzzle(int(line[0]),line[2:])
#         print("Puzzle #"+str(lineNum)+" Children:")
#         for s in getChildren(line[2:],int(line[0])):
#             printPuzzle(int(line[0]),s)
#         print("Goal for puzzle #"+str(lineNum)+": ")
#         printPuzzle(int(line[0]),findGoal(line[2:]))
#         lineNum = lineNum + 1

#Part 4:BFS
def findPossibles(s):
    visited=set()
    fringe=deque()
    length=int(len(s)**0.5)
    visited.add(s)
    fringe.append(s)
    while(len(fringe)>0):
        s1=fringe.popleft()
        for s2 in getChildren(s1,length):
            if(not s2 in visited):
                fringe.append(s2)
                visited.add(s2)
    return len(visited)
# print("Part 4:")
# print("2x2: "+str(findPossibles("ABC.")))
# print("3x3: "+str(findPossibles("12345678.")))

#Part 5
def findShortest(s,line):
    #time
    start=time.perf_counter()
    #
    size = int(len(s) ** 0.5)
    visited = set()
    fringe=deque()
    length=int(len(s)**0.5)
    paths=(s,)
    visited.add(s)
    fringe.append(paths)
    goal=findGoal(s)
    #allPaths=set()
    while(len(fringe)>0):
        path1=fringe.popleft()
        if(path1[-1]==goal):
            #Time
            end=time.perf_counter()
            print("Line "+str(line)+": "+s+str(len(path1)-1)+" moves, " + str(end-start)+" seconds to run")
            print()
            #Printing the path:
            # print("Steps: ")
            # for p in path1:
            #     printPuzzle(size,p)

            return
        for s2 in getChildren(path1[-1],length):
            if(not s2 in visited):
                path2=path1+(s2,)
                fringe.append(path2)
                visited.add(s2)
    return None



#Part 6:
def findHardest(s):
    visited=set()
    lens=[]
    fringe=deque()
    paths=(s,0)
    max=0
    length=int(len(s)**0.5)
    visited.add(s)
    hardest=set()
    fringe.append(paths)
    while(len(fringe)>0):
        s1=fringe.popleft()
        for s2 in getChildren(s1[0],length):
            if(not s2 in visited):
                num=s1[1]+1
                lens.append(num)
                path1=(s2,num)
                if(path1[1]>max):
                    max=path1[1]
                if(path1[1]==31):
                    hardest.add(path1)
                fringe.append(path1)
                visited.add(s2)
    maxNum=0
    for finals in lens:
        if(finals==max):
            maxNum=maxNum+1
    print(str(maxNum)+" puzzles that require "+str(max)+" moves")
    print("hardest:"+str(hardest))



#Part 7:
def findDFS(s):
    #time
    start=time.perf_counter()
    #
    size = int(len(s) ** 0.5)
    visited = set()
    fringe=[]
    length=int(len(s)**0.5)
    paths=(s,)
    visited.add(s)
    fringe.append(paths)
    goal=findGoal(s)
    #allPaths=set()
    while(len(fringe)>0):
        path1=fringe.pop()
        if(path1[-1]==goal):
            #Time
            end=time.perf_counter()
            print("DFS: "+s+": "+str(len(path1)-1)+" moves, " + str(end-start)+" seconds to run")
            #

            #Printing the path:
            # print("Steps: ")
            # for p in path1:
            #     printPuzzle(size,p)

            return
        for s2 in getChildren(path1[-1],length):
            if(not s2 in visited):
                path2=path1+(s2,)
                fringe.append(path2)
                visited.add(s2)
    return None



#main
# findHardest("12345678.")
# findShortest(".25187643",1)
# findDFS(".25187643")

fileName=sys.argv[1]
with open(fileName) as f:
    lineNum=1
    for line in f:
        findShortest(line[2:],lineNum)
        lineNum=lineNum+1
