#Jason Xu - B: Randomization

import heapq
import time
import random

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
    startNode=(Heuristic(s,goal,length),random.randint(1,1000),0,s)
    fringe.append(startNode)
    while(len(fringe)>0):
        node=heapq.heappop(fringe)
        if(node[3]==goal):
            return node[2]
        if(not node[3] in closed):
            closed.add(node[3])
            for child in getChildren(node[3],length):
                h=Heuristic(child,goal,length)
                g=node[2]+1
                randVal=random.randint(1,1000)
                new=(g*mult+h,randVal,g,child)
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

# fileName=sys.argv[1]
# with open(fileName) as f:
#     startAll=time.perf_counter()
#     linenum=0
#     for line in f:
#         if linenum<41:
#             puz = line.strip()
#             print("Line: "+str(linenum))
#             s1 = time.perf_counter()
#             moves=AStar(puz,0.8)
#             e1 = time.perf_counter()
#             print("Astar found "+str(moves)+" moves in " + str(e1-s1)+" seconds")
#             linenum=linenum+1
#     endAll = time.perf_counter()
#     print("Total time: "+str(endAll-startAll))
for i in range(0,100):
    print(AStar("BDHCOFAJIGNKM.EL",0.55))
#Python "A.py" G.txt
