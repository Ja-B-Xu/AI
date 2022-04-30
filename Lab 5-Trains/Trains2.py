#Jason Xu
#Weighted Graph Search with Train Routes

import heapq, time, sys, tkinter
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

window=tkinter.Tk()
window.title("Train Route Lab")
canv = tkinter.Canvas(window,width=800,height=800, bg="black")
canv.pack()
window.update()

###Generate map
for temp in connections:
    for line in connections[temp]:
        y1,x1=nodes[temp][0],nodes[temp][1]
        canv.create_line(1200-abs(float(x1)*8),800-abs(float(y1)*10),1200-abs(float(nodes[line[0]][1])*8),800-abs(float(nodes[line[0]][0])*10),fill="gray")
window.update()
###
def Dijkstra(start,goal):
    goalId=cities[goal]
    startId=cities[start]
    goalcoords=(nodes[goalId][0],nodes[goalId][1])
    startcoords=(nodes[startId][0],nodes[startId][1])
    startNode=(0,startId,(startId,))
    fringe=[]
    closed=set()
    fringe.append(startNode)
    count=0
    limit=100
    while(len(fringe)>0):
        node=heapq.heappop(fringe)
        nodecoords=nodes[node[1]]
        if(nodecoords[0]==goalcoords[0] and nodecoords[1]==goalcoords[1]):
            for pos in range(len(node[2])-1):
                curr=node[2][pos]
                next=node[2][pos+1]
                canv.create_line(1200 - abs(float(nodes[curr][1]) * 8), 800 - abs(float(nodes[curr][0]) * 10),
                                 1200 - abs(float(nodes[next][1]) * 8), 800 - abs(float(nodes[next][0]) * 10),fill="red")
            window.update()
            return node[0]
        if(not node[1] in closed):
            closed.add(node[1])
            for child in connections[node[1]]:
                path=node[2]
                path=path+(child[0],)
                newDist=node[0]+child[1]
                new=(newDist,child[0],path)
                heapq.heappush(fringe,new)
                canv.create_line(1200 - abs(float(nodecoords[1]) * 8), 800 - abs(float(nodecoords[0]) * 10),
                                 1200 - abs(float(nodes[child[0]][1]) * 8), 800 - abs(float(nodes[child[0]][0]) * 10),
                                 fill="blue")
        if(count==limit):
            window.update()
            count=0
            limit=limit+int(limit/4)
        count=count+1
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
    count=0
    limit=100
    while(len(fringe)>0):
        node=heapq.heappop(fringe)
        nodecoords=nodes[node[1]]
        if(nodecoords[0]==goalcoords[0] and nodecoords[1]==goalcoords[1]):
            for pos in range(len(node[2])-1):
                curr=node[2][pos]
                next=node[2][pos+1]
                canv.create_line(1200 - abs(float(nodes[curr][1]) * 8), 800 - abs(float(nodes[curr][0]) * 10),
                                 1200 - abs(float(nodes[next][1]) * 8), 800 - abs(float(nodes[next][0]) * 10),fill="red")
            return node[3]
        if(not node[1] in closed):
            closed.add(node[1])
            for child in connections[node[1]]:
                h=distance(nodes[child[0]],goalcoords)
                path=node[2]
                path=path+(child[0],)
                newDist=node[3]+child[1]
                new=(h+newDist,child[0],path,newDist)
                heapq.heappush(fringe,new)
                canv.create_line(1200-abs(float(nodecoords[1])*8),800-abs(float(nodecoords[0])*10), 1200-abs(float(nodes[child[0]][1])*8), 800-abs(float(nodes[child[0]][0])*10),fill="blue")
        if(count==limit):
            window.update()
            count=0
            limit=limit+50
        count=count+1
    return None

time.sleep(1)
city1,city2=sys.argv[1],sys.argv[2]

val1=Dijkstra(city1,city2)

for temp in connections:
    for line in connections[temp]:
        y1,x1=nodes[temp][0],nodes[temp][1]
        canv.create_line(1200-abs(float(x1)*8),800-abs(float(y1)*10),1200-abs(float(nodes[line[0]][1])*8),800-abs(float(nodes[line[0]][0])*10),fill="gray")
window.update()

val2=AStar(city1,city2)
window.mainloop()
#Python Trains2.py "Merida" "Miami"