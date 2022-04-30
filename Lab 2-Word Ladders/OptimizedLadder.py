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
ss=time.perf_counter()
for sWord in words:
    similars=set()
    for pos in range(len(sWord)):
        temp=list(sWord.strip())
        temp[pos-1]="_"
        for sim in bucket["".join(temp).strip()]:
            similars.add(sim)
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
        p=(starting,)
        fringe.append(p)
        visited.add(starting)
        while(len(fringe)>0 and not solvable):
            path=fringe.popleft()
            current=path[-1]
            if(current==goal):
                solvable=True
                print("Length: "+str(len(path)))
                for one in path:
                    print(one)
            for child in step[current]:
                if(not child in visited):
                    visited.add(child)
                    fringe.append(path+(child,))
        lineNum=lineNum+1
        if(not solvable):
            print("No solution")
        print()
end2=time.perf_counter()
print(str(end2-start2)+" seconds to solve all the puzzles. Total time was "+str(end2-start))
#Python OptimizedLadder.py Dict.txt 6Lets.txt
#Python OptimizedLadder.py LongDict.txt LongPuzzles.txt