#Jason Xu
#Sliding Puzzles Part 1 Outstanding Work-Bidirectional

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


def BFS(s):
    #time
    start=time.perf_counter()
    #
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
            print("BFS: "+s+" "+str(len(path1)-1)+" moves, " + str(end-start)+" seconds to run")
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

def BiBFS(s):
    start = time.perf_counter()
    size=int(len(s)**0.5)
    forwardFringe=deque()
    backFringe=deque()
    forwardVis=set()
    backVis=set()
    goal=findGoal(s)
    forwardVis.add(s)
    backVis.add(goal)
    forwardFringe.append((s,0))
    backFringe.append((goal,0))
    discarded=set()
    while(len(forwardFringe)>0 and len(backFringe)>0):
        curr=forwardFringe.popleft()
        if(curr[0] in backVis):
            for state in backFringe:
                if(state[0]==curr[0]):
                    end = time.perf_counter()
                    print("BiBFS: "+s+" "+str(curr[1]+state[1])+" moves, "+str(end-start)+" seconds to run")
                    return
            for state in discarded:
                if(state[0]==curr[0]):
                    end = time.perf_counter()
                    print("BiBFS: "+s+" "+str(curr[1]+state[1])+" moves, "+str(end-start)+" seconds to run")
                    return
        if(curr[0]==goal):
            end = time.perf_counter()
            print("BiBFS: Line " + str(line) + " " + s + " " + str(curr[1]) + " moves, " + str(
                end - start) + " seconds to run")
        for child in getChildren(curr[0],size):
            if(not child in forwardVis):
                newLen=curr[1]+1
                next=(child,newLen)
                forwardVis.add(child)
                forwardFringe.append(next)
        bcurr=backFringe.popleft()
        discarded.add(bcurr)
        for bchild in getChildren(bcurr[0],size):
            if(not bchild in backVis):
                newLen=bcurr[1]+1
                next=(bchild,newLen)
                backVis.add(bchild)
                backFringe.append(next)
    print("Test")
    return None


#fileName=sys.argv[1]
with open("slide_puzzle_tests.txt") as f:
    lineNum=1
    for line in f:
        print("Line "+str(lineNum))
        BFS(line[2:])
        BiBFS(line[2:])
        print()
        lineNum=lineNum+1
