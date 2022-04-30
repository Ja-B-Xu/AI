# Jason Xu
# Perceptrons part 2

import sys, ast

# A is the function, w is weight vector, b is the bias scalar, and x is the input vector
def perceptron(A, w, b, x):
    num = float(b)
    for i in range(len(w)):
        num += (float(w[i]) * float(x[i]))
    return A(num)


def step(num):
    if num > 0:
        return 1
    return 0


def truthTable(bits, n):
    rows = []
    numrows = 2 ** bits
    binary = bin(n)[2:]
    while len(binary) < numrows:
        binary = "0" + binary
    if len(binary) > numrows:
        print("Value is too high")
        return None
    for val in range(numrows - 1, -1, -1):
        temp = bin(val)[2:]
        while len(temp) < bits:
            temp = "0" + temp
        rowleft = tuple(temp)
        rowright = binary[numrows - val - 1]
        row = (rowleft, rowright)
        rows.append(row)
    return rows


def prettyPrint(table):
    print()
    bits = len(table[0][0])
    toprow = ""
    for i in range(bits):
        toprow += "in" + str(i + 1) + "\t"
    toprow += "| Out"
    rowlen = len(toprow)
    print(toprow)
    bar = "-" * rowlen
    print(bar)
    for row in table:
        rowstr = ""
        for pos in range(bits):
            rowstr += row[0][pos] + "\t"
        rowstr += "| " + row[1]
        print(rowstr)
    print()

# n is the canonical table representation, w is weight vector, b is bias scalar
def check(n, w, b):
    ttable = truthTable(len(w), n)
    perclist = []
    for row in ttable:
        perclist.append(perceptron(step, w, b, row[0]))
    numcorrect = 0
    #print(perclist)
    for pos in range(len(perclist)):
        if perclist[pos] == int(ttable[pos][1]):
            numcorrect += 1
    return numcorrect/len(ttable)


def train(n, w, b, learningrate):
    ttable = truthTable(len(w), n)
    for epochnum in range(100):
        for rownum in range(len(ttable)):
            currentperc = perceptron(step, w, b, ttable[rownum][0])
            if currentperc != int(ttable[rownum][1]):
                diff = int(ttable[rownum][1]) - currentperc
                w, b = update(diff, w, b, ttable[rownum][0], learningrate)
    return w, b


def update(difference, w, b, x, lr):
    factor = difference * lr
    newb = float(b) + factor
    neww = tuple()
    for pos in range(len(w)):
        neww += ((factor * float(x[pos])) + float(w[pos])),
    return neww, newb


def calctotal(bits):
    total = 2 ** (2 ** bits)
    correct = 0
    for i in range(total):
        tempw = ("0",) * bits
        p = train(i, tempw, "0", 1)
        if check(i, p[0], p[1]) == 1:
            correct += 1
    return correct, total


def XOR(x): #XOR HAPPENS HERE
    w13, w23, b3, w14, w24, b4, w35, w45, b5 = 1, 1, 0, -1, -2, 3, 1, 2, -2
    p3 = perceptron(step, (w13, w23), b3, (x[0], x[1]))
    p4 = perceptron(step, (w14, w24), b4, (x[0], x[1]))
    p5 = perceptron(step, (w35, w45), b5, (p3, p4))
    print("XOR result: " + str(p5))



sysinput = sys.argv
if len(sysinput) == 2:
    XOR(ast.literal_eval(sysinput[1]))
elif len(sysinput) == 3:
    wtrain = (0,) * int(sysinput[1])
    result = train(int(sysinput[2]), wtrain, 0, 1)
    print("Weight vecotr: " + str(result[0]))
    print("Bias scalar: " + str(result[1]))
    print("Accuracy: " + str(check(int(sysinput[2]), result[0], result[1])))


# print(train(int(sysinput[1]), ast.literal_eval(sysinput[2]), float(sysinput[3]), 1))