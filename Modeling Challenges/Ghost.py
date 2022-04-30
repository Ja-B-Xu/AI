#Jason Xu and Chen

import sys

input = sys.argv
cur = ""
dic, minLen = input[1], input[2]
if len(input) == 4:
    cur = input[3]


def generateWords(fragment, poss):      #Problem is adding new entire word instead of just one letter
    fragment = fragment.upper()
    new = []
    length = len(fragment)
    for str in poss:
        if str[0:length] == fragment:
            if len(new) > 0:
                temp = new[-1]
                if not str[0:len(temp)] == temp:
                    new.append(str.strip())
            else:
                new.append(str.strip())
    #print(new)
    return new

def nextLet(word, poss):
    lets = set()
    for temp in poss:
        lets.add(word + temp[len(word)])
    return lets


def maxx(word, poss):
    # print(word)
    poss = generateWords(word, poss)
    even = False
    odd = False
    results = []
    wins = []
    for w in poss:
        if (len(w) - len(word)) % 2 == 0:
            even = True
        else:
            odd = True
    if not even:
        return -1, wins
    if not odd:
        return 1, wins
    nexts = list(nextLet(word, poss))
    for w in nexts:
        results.append(minn(w,poss)[0])
    for i in range(len(results)):
        if results[i] == 1:
            wins.append(nexts[i][len(word)])
    if len(wins) > 0:
        return 1, wins
    else:
        return -1, wins

def minn(word, poss):
    # print(word)
    poss = generateWords(word, poss)
    even = False
    odd = False
    results = []
    wins = []
    for w in poss:
        if (len(w) - len(word)) % 2 == 0:
            even = True
        else:
            odd = True
    if not even:
        return 1, wins
    if not odd:
        return -1, wins
    nexts = list(nextLet(word, poss))
    for w in nexts:
        results.append(maxx(w,poss)[0])
    for i in range(len(results)):
        if results[i] == -1:
            wins.append(nexts[i][len(word)])
    if len(wins) > 0:
        return -1, wins
    else:
        return 1, wins

with open(dic) as f:
    newdic = []
    for line in f:
        if line.strip().isalpha() and len(line.strip()) >= int(minLen):
            newdic.append(line.upper().strip())
    result = (maxx(cur,newdic))
    if result[0] == -1:
        print("Next player will lose!")
    else:
        print("Next player can win with any of these letters:\t" + str(result[1]))



#Ghost.py Ghost.txt 4 ABC
#Ghost.py Ghost2.txt 4