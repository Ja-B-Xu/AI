#Jason Xu
#Word Ladders Optimization

import time
from collections import deque
import sys



puzzles=sys.argv[2]
dict=sys.argv[1]


#Building data structure
start=time.perf_counter()
words=set()
step={}
bucket={}
with open(dict) as f:
    for line in f:
        line=line.strip()
        words.add(line)
        for pos in range(len(line)):
            wordList=list(line)
            wordList[pos-1]="_"
            if("".join(wordList) in bucket):
                bucket["".join(wordList)]=bucket["".join(wordList)]+((line,))
            else:
                bucket["".join(wordList)]=(line,)
for sWord in words:
    similars=[]
    for pos in range(len(sWord)):
        temp=list(sWord.strip())
        temp[pos-1]="_"
        for sim in bucket["".join(temp).strip()]:
            similars.append(sim)
    step[sWord.strip()]=similars
end=time.perf_counter()
print(str(end-start)+" seconds to create the data structure.\n")

with open(puzzles) as f:
    lineNum=0
    start2 = time.perf_counter()
    for line in f:
        solvable=False
        print("Line: "+str(lineNum))
        starting, goal=(line.split(" ")[0].strip()), (line.split(" ")[1].strip())
        fringe=deque()
        visited=set()
        fringe.append((starting,))
        visited.add(starting)
        bFringe=deque()
        bVisited=set()
        bVisited.add(goal)
        bFringe.append((goal,))
        discarded=[]
        while(len(fringe)>0 and len(bFringe)>0 and not solvable):
            path=fringe.popleft()
            if(path[-1] in bVisited):
                for state in discarded:
                    if(state[-1]==path[-1]):
                        print("Length: "+str(len(state)+len(path)-1))
                        # for x in path:
                        #     print(x)
                        # for x in state[-2::-1]:
                        #     print(x)
                        solvable=True
                for state in bFringe:
                    if(state[-1]==path[-1]):
                        print("Length: "+str(len(state)+len(path)-1))
                        # for x in path:
                        #     print(x)
                        # for x in state[-2::-1]:
                        #     print(x)
                        solvable=True

            for child in step[path[-1]]:
                if(not child in visited):
                    visited.add(child)
                    newPath=path+(child,)
                    fringe.append(newPath)

            bPath=bFringe.popleft()
            discarded.append(bPath)
            for bChild in step[bPath[-1]]:
                if(not bChild in bVisited):
                    bVisited.add(bChild)
                    newBPath=bPath+(bChild,)
                    bFringe.append(newBPath)

        lineNum=lineNum+1
        if(not solvable):
            print("No solution")
        print()
end2=time.perf_counter()
print(str(end2-start2)+" seconds to solve all the puzzles. Total time was "+str(end2-start))
#Python OptimizedLadderTest.py Dict.txt 6Lets.txt