#Jason Xu
#Perceptrons 4 - Back Propogation

import sys, ast, math, random
import numpy as np


def sigmoid(num):
    num = num * -1
    return (1 / (1 + (math.e) ** num))


def sigmoidDeriv(num):
    sig = sigmoid(num)
    return sig * (1 - sig)




def backProp(A, derivA, tests, wlist, blist, learnrate):
    A = np.vectorize(A)
    derivA = np.vectorize(derivA)
    for epoch in range(5000):
        for test in tests:
            x, y = test[0], test[1]
            alist = [np.array([x])]
            dots = [None]
            delts = [None]
            for layer in range(1, len(wlist)):
                dot_l = (alist[layer - 1] @ wlist[layer]) + blist[layer]
                dots.append(dot_l)
                delts.append(None)
                alist.append(A(dot_l))
            print(str(x) + ":")
            print(alist[-1])
            print()
            delt_n = derivA(dots[-1]) * (y - alist[-1])
            delts[-1] = delt_n
            for layer in range(len(alist) - 2, 0, -1):
                delts[layer] = derivA(dots[layer]) * (delts[layer + 1] @ (wlist[layer + 1].transpose()))
            for layer in range(1, len(wlist)):
                blist[layer] = blist[layer] + (learnrate * delts[layer])
                wlist[layer] = wlist[layer] + (learnrate * ((alist[layer - 1].transpose()) @ delts[layer]))
    return wlist, blist


# x = [2, 3]
# y = [0.8, 1]
def trainSum():
    te = [[[0,0], [0,0]], [[0,1], [0,1]], [[1,0], [0,1]], [[1,1], [1,0]],]
    w = [None, np.array([[-1 + (2 * random.random()), -1 + (2 * random.random())], [-1 + (2 * random.random()), -1 + (2 * random.random())]]), np.array([[-1 + (2 * random.random()), -1 + (2 * random.random())], [-1 + (2 * random.random()), -1 + (2 * random.random())]])]
    b = [None, np.array([-1 + (2 * random.random()), -1 + (2 * random.random())]), np.array([-1 + (2 * random.random()), -1 + (2 * random.random())])]
    neww, newb = backProp(sigmoid, sigmoidDeriv, te, w, b, 0.2)
    print("Final weight matrix: " + str(neww))
    print("Final bias matrix: " + str(newb))


def backPropCirc(A, derivA, tests, wlist, blist, learnrate):
    A = np.vectorize(A)
    derivA = np.vectorize(derivA)
    for epoch in range(35):
        for test in tests:
            x, y = test[0], test[1]
            alist = [np.array([x])]
            dots = [None]
            delts = [None]
            for layer in range(1, len(wlist)):
                dot_l = (alist[layer - 1] @ wlist[layer]) + blist[layer]
                dots.append(dot_l)
                delts.append(None)
                alist.append(A(dot_l))
            delt_n = derivA(dots[-1]) * (y - alist[-1])
            delts[-1] = delt_n
            for layer in range(len(alist) - 2, 0, -1):
                delts[layer] = derivA(dots[layer]) * (delts[layer + 1] @ (wlist[layer + 1].transpose()))
            for layer in range(1, len(wlist)):
                blist[layer] = blist[layer] + (learnrate * delts[layer])
                wlist[layer] = wlist[layer] + (learnrate * ((alist[layer - 1].transpose()) @ delts[layer]))
        incorrect = 0
        for test in tests:
            out = pNet(A, test[0], wlist, blist)
            y = test[1]
            if out >= 0.5 and y == 0:
                incorrect += 1
            if out < 0.5 and y == 1:
                incorrect +=1
        learnrate = 0.0005 * incorrect
        print("Epoch: " + str(epoch))
        print("Number incorrect: " + str(incorrect))
        print()
    return wlist, blist


def rand():
    return -1 + (2 * random.random())

def trainCirc():
    testset = []
    w = [None, np.array([[rand(), rand(), rand(), rand()], [rand(), rand(), rand(), rand()]]), np.array([[rand()], [rand()], [rand()], [rand()]])]
    b = [None, np.array([rand(), rand(), rand(), rand()]), np.array([rand()])]

    with open("10000_pairs.txt") as f:
        for line in f:
            x = line.split(" ")
            x[0], x[1] = float("".join(x[0].split())), float("".join(x[1].split()))
            actual = ((x[0] ** 2) + (x[1] ** 2)) ** 0.5
            if actual >= 1:
                y = 1
            else:
                y = 0
            testset.append(np.array([x, y]))
    print(backPropCirc(sigmoid, sigmoidDeriv, testset, w, b, 0.05))


def pNet(A, x, wlist, blist):
    newA = np.vectorize(A)
    alist = []
    alist.append(x)
    for pos in range(1, len(wlist)):
        output = newA((alist[pos-1]@wlist[pos]) + blist[pos])
        alist.append(output)
    return alist[-1]

sysinput = sys.argv

if sysinput[1] == "S":
    trainSum()
if sysinput[1] == "C":
    trainCirc()