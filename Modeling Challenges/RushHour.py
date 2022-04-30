from collections import deque

########################################################################################################################
#Creating the board
########################################################################################################################
# row0=["1","2","2","3","4","4"]
# row1=["1","5",".","3","6","."]
# row2=["7","5","A","A","6","."]
# row3=["7","5","8",".","9","9"]
# row4=[".",".","8","Q","Q","W"]
# row5=["E","E","E",".",".","W"]

# row0=[".",".","1","1","1","2"]
# row1=[".","3","3",".","4","2"]
# row2=[".","A","A",".","4","5"]
# row3=["6","6","7","7","4","5"]
# row4=[".",".","8","9","9","9"]
# row5=[".",".","8","B","B","B"]

# row0=["1","1","1","4","5","6"]
# row1=["2","3","3","4","5","6"]
# row2=["2",".","A","A","5","6"]
# row3=["8","8","9",".",".","."]
# row4=[".","B","9",".","D","D"]
# row5=[".","B","C","C","E","E"]

row0=["9",".",".","D","D","D"]
row1=["9",".","B","B","C","C"]
row2=["A","A","8",".",".","1"]
row3=["7","7","8","4","3","1"]
row4=["5","5","5","4","3","2"]
row5=["6","6",".",".",".","2"]

# row0=[".",".",".",".",".","."]
# row1=[".",".",".",".",".","."]
# row2=[".",".",".",".",".","."]
# row3=[".",".",".",".",".","."]
# row4=[".",".",".",".",".","."]
# row5=[".",".",".",".",".","."]

board=str("".join(row0).strip()+"".join(row1).strip()+"".join(row2).strip()+"".join(row3).strip()+"".join(row4).strip()+"".join(row5).strip())


########################################################################################################################
#Methods
########################################################################################################################
def display(b):
    current=0
    for pos in range(0,6):
        print(b[current:current+6])
        current=current+6

def solved(b):
    exit=b[12:18]
    carPos=exit.find("A")+2
    if carPos>6:
        return True
    for tile in exit[carPos:]:
        if(not tile=="."):
            return False
    return True

def getCars(b):
    visited=set()
    cars=[]
    for pos in range(len(b)):
        let=b[pos]
        if let!="." and not let in visited:
            visited.add(let)
            car=((pos%6,pos//6),)
            if(pos<35 and b[pos+1]==let):
                newPos=pos+1
                car=car+((newPos%6,newPos//6),)
                if(pos<34 and b[pos+2]==let):
                    newPos=pos+2
                    car=car+((newPos%6,newPos//6),)
            if(pos<30 and b[pos+6]==let):
                newPos=pos+6
                car=car+((newPos%6,newPos//6),)
                if(pos<24 and b[pos+12]==let):
                    newPos=pos+12
                    car=car+((newPos%6,newPos//6),)
            cars.append(car)
    return cars

def getChildren(b,cars):
    children=[]
    for car in cars:
        length=len(car)
        x1,x2=car[0][0],car[1][0]
        if x1==x2: #Vertical car
            let=b[car[0][0]+(6*car[0][1])]
            for pos in range(car[0][1]-1,-1,-1): #Checking upwards
                if b[car[0][0]+6*(pos)]==".":
                    newBoard=list(b)
                    xpos=car[0][0]
                    ypos=[]
                    for ys in car:
                        ypos.append(ys[1])
                    x=0
                    for num in ypos:
                        newBoard[xpos+6*num]="."
                    for num in ypos:
                        newBoard[xpos+6*(pos+x)]=let
                        x=x+1
                    children.append("".join(newBoard).strip())
                else:
                    break
            for pos in range(car[-1][1]+1,6): #Checking downwards
                if b[car[0][0]+6*(pos)]==".":
                    newBoard=list(b)
                    xpos=car[0][0]
                    ypos=[]
                    for ys in car:
                        ypos.append(ys[1])
                    x=0
                    for num in ypos:
                        newBoard[xpos+6*num]="."
                    for num in ypos:
                        newBoard[xpos+6*(pos-x)]=let
                        x=x+1
                    children.append("".join(newBoard).strip())
                else:
                    break
        else: #Horizontal car
            let = b[car[0][0] + (6 * car[0][1])]
            for pos in range(car[0][0]-1,-1,-1): #Checking left
                yval=6*car[0][1]
                if b[pos+yval]==".":
                    newBoard = list(b)
                    xpos = []
                    for xs in car:
                        xpos.append(xs[0])
                    bruh=0
                    for num in xpos:
                        newBoard[num+yval] = "."
                    for num in xpos:
                        newBoard[pos+yval+bruh] = let
                        bruh=bruh+1
                    children.append("".join(newBoard).strip())
                else:
                    break

            for pos in range(car[-1][0]+1,6): #Checking right
                yval=6*car[0][1]
                if b[pos+yval]==".":
                    newBoard = list(b)
                    xpos = []
                    for xs in car:
                        xpos.append(xs[0])
                    bruh=0
                    for num in xpos:
                        newBoard[num+yval] = "."
                    for num in xpos:
                        newBoard[pos+yval-bruh] = let
                        bruh=bruh+1
                    children.append("".join(newBoard).strip())
                else:
                    break

    return children

def BFS(b):
    visited = set()
    fringe=deque()
    start=(b,)
    visited.add(b)
    fringe.append(start)
    while(len(fringe)>0):
        popped=fringe.popleft()
        current=popped[-1]
        if(solved(current)):
            return len(popped),popped
        cars=getCars(current)
        for child in getChildren(current,cars):
            if not child in visited:
                visited.add(child)
                new=popped+(child,)
                fringe.append(new)
    return None

########################################################################################################################
#Main
########################################################################################################################
number,moves=BFS(board)
print(number)

for state in moves:
    display(state)
    print()