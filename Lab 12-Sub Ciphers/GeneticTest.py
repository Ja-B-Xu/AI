#Jason Xu
#Genetic Algorithm on Substituion Ciphers

import random, sys, math

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#teststr = "ZFNNANWJWYBZLKEHBZTNSKDDGJWYLWSBFNSSJWYFNKBGLKOCNKSJEBDWZFNGKLJKJNQFJPFJBXHBZTNRDKNZFNPDEJWYDRPDEGCNZNWJYFZZFLZTCNBBNBZFNNLKZFSLKONWBLCCKJANKBPHGBZFNGNLOBLWSRDCSBZFNRJWLCBFDKNJWLWSWDTDSUWDTDSUOWDQBQFLZBYDJWYZDFLGGNWZDLWUTDSUTNBJSNBZFNRDKCDKWKLYBDRYKDQJWYDCSJZFJWODRSNLWEDKJLKZUJNANWZFJWODRDCSSNLWEDKJLKZUZFNRLZFNKQNWNANKRDHWSJZFJWODRSNLWEDKJLKZU"

popsize = 300
clones = 1
tournsize = 20
tournwin = 0.75
crossovers = 5
mutationrate = 0.8
nvalue = 3
ngrams = {}
ngrams2 = {}
ngrams3 = {}


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
    current = 0
    for line in file:
        if str(nvalue) + "-gram" in line:
            current = 1
        elif str(nvalue + 1) + "-gram" in line:
            current = 2
        elif str(nvalue + 2) + "-gram" in line:
            current = 3
        elif str(nvalue + 3) + "-gram" in line:
            break
        elif current == 1:
            pieces = line.split("\t")
            ngrams[pieces[0]] = math.log2(int(pieces[1]))
        elif current == 2:
            pieces = line.split("\t")
            ngrams2[pieces[0]] = math.log2(int(pieces[1]))
        elif current == 3:
            pieces = line.split("\t")
            ngrams3[pieces[0]] = math.log2(int(pieces[1]))



def findVal(word, cipher): #Fitness Function
    score = 0
    word = decode(word, cipher)
    for pos in range(len(word) - nvalue + 1):
        gram = word[pos:pos + nvalue].upper()
        if gram.isalpha():
            if gram in ngrams.keys():
                score += ngrams[gram]
        if (len(word) - pos) >= nvalue:
            gram = word[pos:pos + nvalue + 1].upper()
            if gram.isalpha():
                if gram in ngrams2.keys():
                    score += ngrams2[gram]
        if (len(word) - pos) > nvalue:
            gram = word[pos:pos + nvalue + 2].upper()
            if gram.isalpha():
                if gram in ngrams3.keys():
                    score += ngrams3[gram]
    score = math.log2(score)
    return score


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
            nextgen.append(child)
            num += 1
    return nextgen


def firstGen():
    gen1 = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"] * popsize
    for g in range(len(gen1)):
        glist = list(gen1[g])
        random.shuffle(glist)
        gen1[g] = "".join(glist)
    return(gen1)


def genAlg(code, population, gennum):
    fitnesses = {}
    fitlist = []
    for single in population:
        val = findVal(teststr, single)
        fitnesses[single] = val
        fitlist.append(val)
    sortedstrats = [x for _, x in sorted(zip(fitlist, population))]
    print(str(gennum) + ": " + decode(code, sortedstrats[-1]))
    nextg = selectNext(population, fitnesses, sortedstrats)
    genAlg(code, nextg, gennum + 1)


teststr = sys.argv[1]
findgrams("ngrams1.tsv")
first = firstGen()
genAlg(teststr, first, 1)
# testcipher = "XRPHIWGSONFQDZEYVJKMATUCLB"
# enc = encode("testing encoded cipher", testcipher)
# print(enc)
# print(decode(enc, testcipher))
# print(findVal("TION"))
# teststrats = ["XRPHIWGSONFQDZEYVJKMATUCLB", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
# print(testval1)
# print(testval2)
# testfits = {"XRPHIWGSONFQDZEYVJKMATUCLB": testval1, "ABCDEFGHIJKLMNOPQRSTUVWXYZ":testval2}
# print(tournament(teststrats, testfits)
# print(breed("XRPHIWGSONFQDZEYVJKMATUCLB", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))