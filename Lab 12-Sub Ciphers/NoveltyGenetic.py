#Jason Xu
#Genetic Algorithm on Substituion Ciphers, attempting to use a novelty score.

import random, sys, math
import Levenshtein
from difflib import get_close_matches
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#teststr = "ZFNNANWJWYBZLKEHBZTNSKDDGJWYLWSBFNSSJWYFNKBGLKOCNKSJEBDWZFNGKLJKJNQFJPFJBXHBZTNRDKNZFNPDEJWYDRPDEGCNZNWJYFZZFLZTCNBBNBZFNNLKZFSLKONWBLCCKJANKBPHGBZFNGNLOBLWSRDCSBZFNRJWLCBFDKNJWLWSWDTDSUWDTDSUOWDQBQFLZBYDJWYZDFLGGNWZDLWUTDSUTNBJSNBZFNRDKCDKWKLYBDRYKDQJWYDCSJZFJWODRSNLWEDKJLKZUJNANWZFJWODRDCSSNLWEDKJLKZUZFNRLZFNKQNWNANKRDHWSJZFJWODRSNLWEDKJLKZU"

popsize = 150
clones = 1
tournsize = 20
tournwin = 0.75
crossovers = 5
mutationrate = 0.8
noveltymod = 0.002
nvalue = 3
ngrams = {}
prevciphers = {}
genlist = []
repeateds = []


def encode(decoded, cipher):
    encoded = ""
    for let in decoded:
        if let.isalpha():
            pos = alphabet.find(let.upper())
            encoded += cipher[pos]
        else:
            encoded += let
    return encoded


def decode(encoded, cipher):
    decoded = ""
    for let in encoded:
        if let.isalpha():
            pos = cipher.find(let.upper())
            decoded += alphabet[pos]
        else:
            decoded += let
    return decoded


def findgrams(filename):
    file = open(filename)
    current = False
    count = 0
    for line in file:
        if str(nvalue + 1) + "-gram" in line:
            break
        if current:
            pieces = line.split("\t")
            ngrams[pieces[0]] = math.log2(int(pieces[1]))
            count += 1
        if str(nvalue) + "-gram" in line:
            current = True
    return count


def findVal(word, cipher, pop): #Fitness Function
    score = 0
    word = decode(word, cipher)
    for pos in range(len(word) - nvalue + 1):
        gram = word[pos:pos + nvalue].upper()
        if gram.isalpha():
            if gram in ngrams.keys():
                score += ngrams[gram]
    if len(genlist) < 200 and len(genlist) > 50:
        score = score + (noveltyScore(cipher, pop) * numgrams * noveltymod)
    if len(genlist) < 450 and len(genlist) > 350:
        score = score + (noveltyScore(cipher, pop) * numgrams * noveltymod)
    if len(genlist) > 10:
        if cipher == genlist[-1] == genlist[-2] == genlist[-3] == genlist[-4]:
            repeateds.append(cipher)
            score = -9999
        elif cipher in repeateds:
            score = -9999999
    return score


def noveltyScore(cipher, pop):
    score = Levenshtein.distance(cipher, genlist[-5]) + Levenshtein.distance(cipher, genlist[-10])
    #print(score)
    return score - (prevciphers[cipher] * 10)

# strategies: list of the strats in the tourney, fitnesses: dict of strat:fit
def tournament(strategies, fitnesses):
    fits = []
    for strat in strategies:
        fits.append(fitnesses[strat])
    sortedstrats = [x for _,x in sorted(zip(fits, strategies))]
    sortedstrats.reverse()
    #print(sortedstrats)
    for s in sortedstrats:
        if random.random() < tournwin:
            return s
    return sortedstrats[-1]


def mutate(child):
    pos1 = random.randint(0, 25)
    pos2 = random.randint(0, 25)
    temp = child[pos1]
    child[pos1] = child[pos2]
    child[pos2] = temp
    return child


def breed(dad, mom):
    child = [None] * 26
    crosses = 0
    while crosses < crossovers:
        pos = random.randint(0,25)
        if child[pos] is None:
            crosses += 1
            child[pos] = dad[pos]
    for mompos in range(len(mom)):
        if mom[mompos] not in child:
            nonepos = child.index(None)
            child[nonepos] = mom[mompos]
    if None in child:
        print("breeding error lol")
        return None
    mutval = random.random()
    while mutval < mutationrate:
        child = mutate(child)
        mutval = random.random()
    return "".join(child)


def selectNext(allstrats, allfits, sortedstrats):
    nextgen = []
    sortedstrats.reverse()
    for i in range(clones):
        nextgen.append(sortedstrats[i])
        if sortedstrats[i] in prevciphers.keys():
            prevciphers[sortedstrats[i]] += 1
        else:
            prevciphers[sortedstrats[i]] = 1
    num = 0
    while num < (popsize - clones):
        tourney1, tourney2 = [], []
        while len(tourney1) < tournsize:
            pos = random.randint(0, popsize - 1)
            if allstrats[pos] not in tourney1:
                tourney1.append(allstrats[pos])
        while len(tourney2) < tournsize:
            pos = random.randint(0, popsize - 1)
            if allstrats[pos] not in tourney2 and allstrats[pos] not in tourney1:
                tourney2.append(allstrats[pos])
        parent1 = tournament(tourney1, allfits)
        parent2 = tournament(tourney2, allfits)
        child = breed(parent1, parent2)
        while child in nextgen:
            child = breed(parent1, parent2)
        if child not in nextgen:
            if child in prevciphers.keys():
                prevciphers[child] += 1
            else:
                prevciphers[child] = 1
            nextgen.append(child)
            num += 1
    return nextgen


def firstGen():
    gen1 = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"] * popsize
    for g in range(len(gen1)):
        glist = list(gen1[g])
        random.shuffle(glist)
        gen1[g] = "".join(glist)
        prevciphers[gen1[g]] = 1
    return(gen1)


def genAlg(code, population, gennum):
    fitnesses = {}
    fitlist = []
    for single in population:
        val = findVal(teststr, single, population)
        fitnesses[single] = val
        fitlist.append(val)
    sortedstrats = [x for _, x in sorted(zip(fitlist, population))]
    print(str(gennum) + ": " + decode(code, sortedstrats[-1]))
    print(fitnesses[sortedstrats[-1]])
    genlist.append(sortedstrats[-1])
    nextg = selectNext(population, fitnesses, sortedstrats)
    genAlg(code, nextg, gennum + 1)


teststr = sys.argv[1]
numgrams = findgrams("ngrams1.tsv")
print(numgrams)
first = firstGen()
genAlg(teststr, first, 1)
