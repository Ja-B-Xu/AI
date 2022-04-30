#Jason Xu
#Weighted Graph Search with Train Routes

import heapq, time, sys
from math import pi , acos , sin , cos
#

def distance(set1,set2):
    return GCD(set1[0],set1[1],set2[0],set2[1])
def GCD(y1,x1, y2,x2):
   #
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees

   # if (and only if) the input is strings
   # use the following conversions

   y1  = float(y1)
   x1  = float(x1)
   y2  = float(y2)
   x2  = float(x2)
   #
   R   = 3958.76 # miles = 6371 km
   #
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   #
   # approximate great circle distance with law of cosines
   #
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R
   #

nodes={}
connections={}
cities={}
with open("rrNodes.txt") as f:
    for line in f:
        id=line.split(" ")[0].strip()
        coords=(line.split(" ")[1].strip(),line.split(" ")[2].strip())
        nodes[id]=coords
with open("rrEdges.txt") as f:
    for line in f:
        node1=line.split(" ")[0].strip()
        node2=line.split(" ")[1].strip()
        dist=distance(nodes[node1],nodes[node2])
        part1,part2=(node2,dist),(node1,dist)
        if node1 in connections:
            connections[node1].append(part1)
        else:
            connections[node1]=[part1,]
        if node2 in connections:
            connections[node2].append(part2)
        else:
            connections[node2]=[part2,]
with open("rrNodeCity.txt") as f:
    for line in f:
        id = line.split(" ")[0]
        name=str(line).replace(id,"").strip()
        cities[name]=id

def Dijkstra(start,goal):
    goalId=cities[goal]
    startId=cities[start]
    goalcoords=(nodes[goalId][0],nodes[goalId][1])
    startcoords=(nodes[startId][0],nodes[startId][1])
    startDist=distance(goalcoords,startcoords)
    startNode=(0,startId,(startId,))
    fringe=[]
    closed=set()
    fringe.append(startNode)
    while(len(fringe)>0):
        node=heapq.heappop(fringe)
        nodecoords=nodes[node[1]]
        if(nodecoords[0]==goalcoords[0] and nodecoords[1]==goalcoords[1]):
            return node[0]
        if(not node[1] in closed):
            closed.add(node[1])
            for child in connections[node[1]]:
                path=node[2]
                path=path+(child,)
                newDist=node[0]+child[1]
                new=(newDist,child[0],path)
                heapq.heappush(fringe,new)
    return None

def AStar(start,goal):
    goalId=cities[goal]
    startId=cities[start]
    goalcoords=(nodes[goalId][0],nodes[goalId][1])
    startcoords=(nodes[startId][0],nodes[startId][1])
    startDist=distance(goalcoords,startcoords)
    startNode=(startDist,startId,(startId,),0)
    fringe=[]
    closed=set()
    fringe.append(startNode)
    while(len(fringe)>0):
        node=heapq.heappop(fringe)
        nodecoords=nodes[node[1]]
        if(nodecoords[0]==goalcoords[0] and nodecoords[1]==goalcoords[1]):
            return node[3]
        if(not node[1] in closed):
            closed.add(node[1])
            for child in connections[node[1]]:
                h=distance(nodes[child[0]],goalcoords)
                path=node[2]
                path=path+(child,)
                newDist=node[3]+child[1]
                new=(h+newDist,child[0],path,newDist)
                heapq.heappush(fringe,new)
    return None

city1,city2=sys.argv[1],sys.argv[2]

start1=time.perf_counter()
val1=Dijkstra(city1,city2)
end1=time.perf_counter()
print(city1 + " to " + city2 + " with Dijkstra: " + str(val1) + " in " + str(end1-start1) + " seconds.")
val2=AStar(city1,city2)
end2=time.perf_counter()
print(city1 + " to " + city2 + " with A*: " + str(val2) + " in " + str(end2-end1) + " seconds.")

#Python Trains1.py "Ciudad Juarez" "Montreal"