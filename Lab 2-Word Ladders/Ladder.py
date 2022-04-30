#Jason Xu
#Word Ladders

import time
from collections import deque
import sys



puzzles=sys.argv[2]
dict=sys.argv[1]


#Building data structure
start=time.perf_counter()
words=set()
step={}
alpha="abcdefghijklmnopqrstuvwxyz"
with open(dict) as f:
    for line in f:
        words.add(line)
for sWord in words:
    similars=set()
    for pos in range(len(sWord)):
        for let in alpha:
            temp=list(sWord)
            temp[pos]=let
            if("".join(temp) in words):
                similars.add("".join(temp).replace("\n",""))
    step[sWord.replace("\n","")]=similars
end=time.perf_counter()
print(str(end-start)+" seconds to create the data structure.\n")


with open(puzzles) as f:
    lineNum=0
    start = time.perf_counter()
    for line in f:
        solvable=False
        print("Line: "+str(lineNum))
        starting, goal=(line.split(" ")[0].strip()), (line.split(" ")[1].strip())
        fringe=deque()
        visited=set()
        p=(starting,)
        fringe.append(p)
        visited.add(starting)
        while(len(fringe)>0):
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
    end=time.perf_counter()
    print(str(end-start)+" seconds to solve all the puzzles.\n")
