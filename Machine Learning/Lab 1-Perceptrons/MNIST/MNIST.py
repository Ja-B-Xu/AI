#Jason Xu
#MNIST Training


import sys, ast, math, random, csv
import numpy as np


def sigmoid(num):
    num = num * -1
    if num > 705:
        num = 705
    return 1 / (1 + (math.e) ** num)


def sigmoidDeriv(num):
    sig = sigmoid(num)
    return sig * (1 - sig)


def error(y, afinal):
    nums = y - afinal
    return (np.linalg.norm(nums) ** 2) * 0.5


def backProp(A, derivA, tests, wlist, blist, learnrate):
    A = np.vectorize(A)
    derivA = np.vectorize(derivA)
    for epoch in range(1):
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
    return wlist, blist


def create(parameters):
    wlist = [None]
    blist = [None]
    for index in range(len(parameters) - 1):
        val1 = parameters[index]
        val2 = parameters[index + 1]
        neww = 2 * np.random.rand(val1, val2) - 1
        newb = 2 * np.random.rand(1, val2) - 1
        wlist.append(neww)
        blist.append(newb)
    return wlist, blist


def train(trainname, testname, learnrate, load, epochs, parameters):
    tests = []
    trains = []
    with open(trainname) as f:
        reader = csv.reader(f, delimiter = ",")
        for line in reader:
            ypos = int(line[0])
            y = [0] * 10
            y[ypos] = 1
            x = line[1:]
            for xi in range(len(x)):
                x[xi] = float(x[xi]) / 255
            trains.append([x, y])
    with open(testname) as t:
        reader = csv.reader(t, delimiter = ",")
        for line in reader:
            y = int(line[0])
            x = line[1:]
            for xi in range(len(x)):
                x[xi] = float(x[xi]) / 255
            tests.append([x, y])
    print("start")
    if load:
        currentw, currentb = loadData()
    else:
        currentw, currentb = None, None
    for iteration in range(epochs):
        if currentw is None:
            randoms = create(parameters)
            currentw, currentb = backProp(sigmoid, sigmoidDeriv, trains, randoms[0], randoms[1], learnrate)
        else:
            currentw, currentb = backProp(sigmoid, sigmoidDeriv, trains, currentw, currentb, learnrate)
        np.savetxt("MNIST_WVals1.csv", currentw[1], delimiter = ", ")
        np.savetxt("MNIST_BVals1.csv", currentb[1], delimiter = ", ")
        np.savetxt("MNIST_WVals2.csv", currentw[2], delimiter = ", ")
        np.savetxt("MNIST_BVals2.csv", currentb[2], delimiter = ", ")
        np.savetxt("MNIST_WVals3.csv", currentw[3], delimiter = ", ")
        np.savetxt("MNIST_BVals3.csv", currentb[3], delimiter = ", ")

        print("End of epoch " + str(iteration))
        correct = 0.0
        for tes in tests:
            actual = tes[1]
            result = list(pNet(sigmoid, tes[0], currentw, currentb)[0])
            maxpos = result.index(max(result))
            if maxpos == actual:
                correct += 1
        print("Percentage correctly identified: " + str((correct / len(tests)) * 100))


def loadData():
    w1 = np.loadtxt(open("MNIST_WVals1.csv", "rb"), delimiter = ",")
    w2 = np.loadtxt(open("MNIST_WVals2.csv", "rb"), delimiter=",")
    w3 = np.loadtxt(open("MNIST_WVals3.csv", "rb"), delimiter=",")
    b1 = np.loadtxt(open("MNIST_BVals1.csv", "rb"), delimiter=",")
    b2 = np.loadtxt(open("MNIST_BVals2.csv", "rb"), delimiter=",")
    b3 = np.loadtxt(open("MNIST_BVals3.csv", "rb"), delimiter=",")
    w = [None, w1, w2, w3]
    b = [None, b1, b2, b3]
    return w, b


def pNet(A, x, wlist, blist):
    newA = np.vectorize(A)
    alist = []
    alist.append(x)
    for pos in range(1, len(wlist)):
        output = newA((alist[pos-1]@wlist[pos]) + blist[pos])
        alist.append(output)
    return alist[-1]

# testx = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,18,18,18,126,136,175,26,166,255,247,127,0,0,0,0,0,0,0,0,0,0,0,0,30,36,94,154,170,253,253,253,253,253,225,172,253,242,195,64,0,0,0,0,0,0,0,0,0,0,0,49,238,253,253,253,253,253,253,253,253,251,93,82,82,56,39,0,0,0,0,0,0,0,0,0,0,0,0,18,219,253,253,253,253,253,198,182,247,241,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,80,156,107,253,253,205,11,0,43,154,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,1,154,253,90,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,139,253,190,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,190,253,70,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,35,241,225,160,108,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,81,240,253,253,119,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,45,186,253,253,150,27,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,93,252,253,187,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,249,253,249,64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,46,130,183,253,253,207,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,39,148,229,253,253,253,250,182,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,24,114,221,253,253,253,253,201,78,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,23,66,213,253,253,253,253,198,81,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,18,171,219,253,253,253,253,195,80,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,55,172,226,253,253,253,253,244,133,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,136,253,253,253,212,135,132,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# testset = create([784, 300, 100, 10])
# yeet = list(pNet(sigmoid, testx, testset[0], testset[1])[0])
# print(yeet.index(max(yeet)))
train("MNIST_Train.csv", "MNIST_Test.csv", 0.005, True, 200, [784, 300, 100, 10])
