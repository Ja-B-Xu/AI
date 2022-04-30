from collections import deque
import heapq
import time
import sys

def parity(s,size):
    s1=s.replace(".","").strip()
    score=0
    pos=1
    for let in s1:
        for let2 in s1[pos:]:
            if(let>let2):
                score=score+1
        pos=pos+1
    if(size%2==1):
        return score%2==0
    else:
        if((s.index(".")//size)%2==0):
            return score%2==1
        else:
            return score%2==0


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

def coordToPos(x,y,len):
    return (len*(y-1))+x-1

def posToCoord(x,len):
    return x%len+1,int(x/len+1)

def BFS(s):
    numNodes = 0
    visited = set()
    fringe=deque()
    length=int(len(s)**0.5)
    paths=(s,)
    visited.add(s)
    fringe.append(paths)
    goal=findGoal(s)

    while(len(fringe)>0):
        numNodes = numNodes + 1
        path1=fringe.popleft()
        if(path1[-1]==goal):
            return len(path1)-1,numNodes
        for s2 in getChildren(path1[-1],length):
            if(not s2 in visited):
                path2=path1+(s2,)
                fringe.append(path2)
                visited.add(s2)
    print("Not solvable")
    return None

def IDDFS(s):
    num=0
    result=tuple()
    level=1
    goal = findGoal(s)
    while(len(result)<2):
        result=ID(s,level,goal)
        level=level+1
        num=num+result[0]
    return result[0],num

def ID(s,level,goal):
    numNodes=0
    length = int(len(s) ** 0.5)
    fringe=[]
    start=(0,s,{s,})
    fringe.append(start)
    while(len(fringe)>0):
        numNodes = numNodes + 1
        node=fringe.pop()
        if(node[1]==goal):
            return node[0],numNodes
        if(node[0]<level):
            for child in getChildren(node[1],length):
                if(not child in node[2]):
                    new=(node[0]+1,child,node[2].union({child,}))
                    fringe.append(new)
    return (numNodes,)

def AStar(s):
    numNodes = 0
    length = int(len(s) ** 0.5)
    goal = findGoal(s)
    fringe=[]
    closed=set()
    startNode=(Heuristic(s,goal,length),0,s)
    fringe.append(startNode)
    while(len(fringe)>0):
        numNodes=numNodes+1
        node=heapq.heappop(fringe)
        if(node[2]==goal):
            return node[1],numNodes
        if(not node[2] in closed):
            closed.add(node[2])
            for child in getChildren(node[2],length):
                h=Heuristic(child,goal,length)
                g=node[1]+1
                new=(g+h,g,child)
                heapq.heappush(fringe,new)
    return None

def Heuristic(s,goal,length):
    total=0
    for pos in range(len(goal)):
        if(goal[pos]!="."):
            x=pos%length
            y=pos//length
            let = goal[pos]
            pos2=s.find(let)
            x2=pos2%length
            y2=pos2//length
            total=total+abs(x2-x)+abs(y2-y)
    return total


#Main

fileName=sys.argv[1]
with open(fileName) as f:
    linenum=0
    for line in f:
        length=line.split(" ")[0].strip()
        puz = line.split(" ")[1].strip()
        type = line.split(" ")[2].strip()

        print("Line "+str(linenum))
        start = time.perf_counter()
        if(parity(puz,int(length))):
            if(type=="B"):
                solution,nodes = BFS(puz)
                end = time.perf_counter()
                print("BFS found "+str(solution)+" moves found in "+str(end-start)+" seconds and processed "+ str(nodes//(end-start))+" nodes/sec")
            if(type=="I"):
                solution,nodes = BFS(puz)
                end = time.perf_counter()
                print("IDDFS found "+str(solution)+" moves found in "+str(end-start)+" seconds and processed "+ str(nodes//(end-start))+" nodes/sec")
            if(type == "A"):
                solution,nodes=AStar(puz)
                end = time.perf_counter()
                print("A* found "+str(solution)+" moves found in "+str(end-start)+" seconds and processed "+ str(nodes//(end-start))+" nodes/sec")
            if(type == "!"):
                solution1,nodes1 = BFS(puz)
                end1=time.perf_counter()
                solution2,nodes2 = IDDFS(puz)
                end2=time.perf_counter()
                solution3,nodes3 = AStar(puz)
                end3=time.perf_counter()
                print("BFS found "+str(solution1)+" moves found in "+str(end1-start)+" seconds and processed "+ str(nodes1//(end1-start))+" nodes/sec")
                print("IDDFS found "+str(solution2)+" moves found in "+str(end2-end1)+" seconds and processed "+ str(nodes2//(end2-end1))+" nodes/sec")
                print("A* found "+str(solution3)+" moves found in "+str(end3-end2)+" seconds and processed "+ str(nodes3//(end3-end2))+" nodes/sec")
        else:
            end = time.perf_counter()
            print("No solution found in "+str(end-start)+" seconds")
        linenum=linenum+1
        print()

#Python D.py D.txt