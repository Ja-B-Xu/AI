# Jason Xu
#Gradient Descent

import sys


def funcA(x, y):
    return (4 * (x ** 2)) - (3 * x * y) + (2 * (y ** 2)) + (24 * x) - (20 * y)

def funcAX(x, y):
    return (8 * x) - (3 * y) + 24

def funcAY(x, y):
    return (-3 * x) + (4 * y) - 20

def funcB(x, y):
    return ((1 - y) ** 2) + ((x - (y ** 2)) ** 2)

def funcBX(x, y):
    return 2 * (x - (y ** 2))

def funcBY(x, y):
    return 2 * ((-2 * x * y) + (2 * (y ** 3)) + y - 1)

def minA():
    x = 0
    y = 0
    learnrate = 0.001
    partX = funcAX(x, y)
    partY = funcAY(x, y)
    while ((partX ** 2) + (partY ** 2)) ** 0.5 > 0.00000001:
        grad = [funcAX(x, y), funcAY(x, y)]
        x -= (partX * learnrate)
        y -= (partY * learnrate)
        partX = funcAX(x, y)
        partY = funcAY(x, y)
        print("Position: " + str(x) + ", " + str(y) + ", " + str(funcA(x, y)))
        print("Gradient vector: " + str(grad))
        print()

def minB():
    x = 0
    y = 0
    learnrate = 0.001
    partX = funcBX(x, y)
    partY = funcBY(x, y)
    while ((partX ** 2) + (partY ** 2)) ** 0.5 > 0.00000001:
        grad = [funcBX(x, y), funcBY(x, y)]
        x -= (partX * learnrate)
        y -= (partY * learnrate)
        partX = funcBX(x, y)
        partY = funcBY(x, y)
        print("Position: " + str(x) + ", " + str(y) + ", " + str(funcB(x,y)))
        print("Gradient vector: " + str(grad))
        print()

aorb = sys.argv[1]

if aorb == "A":
    minA()
if aorb == "B":
    minB()

