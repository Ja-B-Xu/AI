#Jason Xu
#I did explorations A, B, D, and G
#Part A Starts on line 8 and includes all the helper methods
#Part B Starts on line 130
#Part D Starts on line 171
#Part G Starts on line 264

#Part A

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

def AStar(s,mult):
    length = int(len(s) ** 0.5)
    goal = findGoal(s)
    fringe=[]
    closed=set()
    startNode=(Heuristic(s,goal,length),0,s)
    fringe.append(startNode)
    while(len(fringe)>0):
        node=heapq.heappop(fringe)
        if(node[2]==goal):
            return node[1]
        if(not node[2] in closed):
            closed.add(node[2])
            for child in getChildren(node[2],length):
                h=Heuristic(child,goal,length)
                g=node[1]+1
                new=(g*mult+h,g,child)
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
    startAll=time.perf_counter()
    linenum=0
    for line in f:
        if linenum<41:
            puz = line.strip()
            print("Line: "+str(linenum))
            s1 = time.perf_counter()
            moves=AStar(puz,0.8)
            e1 = time.perf_counter()
            print("Astar found "+str(moves)+" moves in " + str(e1-s1)+" seconds")
            linenum=linenum+1
    endAll = time.perf_counter()
    print("Total time: "+str(endAll-startAll))


#Part B
#
#
#
    def AStar(s, mult):
        length = int(len(s) ** 0.5)
        goal = findGoal(s)
        fringe = []
        closed = set()
        startNode = (Heuristic(s, goal, length), random.randint(1, 1000), 0, s)
        fringe.append(startNode)
        while (len(fringe) > 0):
            node = heapq.heappop(fringe)
            if (node[3] == goal):
                return node[2]
            if (not node[3] in closed):
                closed.add(node[3])
                for child in getChildren(node[3], length):
                    h = Heuristic(child, goal, length)
                    g = node[2] + 1
                    randVal = random.randint(1, 1000)
                    new = (g * mult + h, randVal, g, child)
                    heapq.heappush(fringe, new)
        return None


    def Heuristic(s, goal, length):
        total = 0
        for pos in range(len(goal)):
            if (goal[pos] != "."):
                x = pos % length
                y = pos // length
                let = goal[pos]
                pos2 = s.find(let)
                x2 = pos2 % length
                y2 = pos2 // length
                total = total + abs(x2 - x) + abs(y2 - y)
        return total


#Part D
#
#
#
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

#Part G
#
#
#
def AStarBucket(s):
    buckets={}
    length = int(len(s) ** 0.5)
    goal = findGoal(s)
    closed=set()
    startVal=Heuristic(s,goal,length)
    startNode=(startVal,0,s)
    buckets[startVal]=[startNode,]
    while(buckets):
        minVal=min(buckets.keys())
        nodes=buckets.pop(minVal)
        node=nodes.pop()
        if(len(nodes)>0):
            buckets[minVal]=nodes
        if(node[2]==goal):
            return node[1]
        if(not node[2] in closed):
            closed.add(node[2])
            for child in getChildren(node[2],length):
                h=Heuristic(child,goal,length)
                g=node[1]+1
                new=(g+h,g,child)
                if not g+h in buckets:
                    buckets[g+h]=[new,]
                else:
                    buckets[g+h].append(new)
    return None

def AStar(s):
    length = int(len(s) ** 0.5)
    goal = findGoal(s)
    fringe=[]
    closed=set()
    startNode=(Heuristic(s,goal,length),0,s)
    fringe.append(startNode)
    while(len(fringe)>0):
        node=heapq.heappop(fringe)
        if(node[2]==goal):
            return node[1]
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
        puz = line.strip()
        print("Line: "+str(linenum))
        s1 = time.perf_counter()
        moves=AStar(puz)
        e1 = time.perf_counter()
        print("Astar using heaps found "+str(moves)+" moves in " + str(e1-s1)+" seconds")
        moves=AStarBucket(puz)
        e2 = time.perf_counter()
        print("Astar using buckets found " + str(moves) + " moves in " + str(e2 - e1) + " seconds")
        linenum=linenum+1