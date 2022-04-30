# Jason Xu
# Perceptrons part 1

import sys, ast

# A is the function, w is weight vector, b is the bias scalar, and x is the input vector
def perceptron(A, w, b, x):
    num = b
    for i in range(len(w)):
        num += (w[i] * float(x[i]))
    return A(num)


def step(num):
    result = int(num + 0.99)
    if result > 1:
        return 1
    if result < 0:
        return 0
    return(int(num + 0.99))


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
    return str(100 * numcorrect/len(ttable)) + "%"


sysinput = sys.argv

print(check(int(sysinput[1]), ast.literal_eval(sysinput[2]), float(sysinput[3])))

