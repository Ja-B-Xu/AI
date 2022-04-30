import nltk
#from nltk.book import *
#from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
# import re
# from urllib import request
#
# url = "https://www.bbc.co.uk"
# response = request.urlopen(url)
# raw = response.read().decode('utf8')
# type(raw)
# tx = re.sub(r'\<script(?:.|\n)*?\<\/script\>', '', raw)
# tx1 = re.sub(r'\<style(?:.|\n)*?\<\/style\>', '', tx)
# temp = re.findall(r'[\s\(\[\{]([a-z]+)', tx1)
# words = nltk.corpus.words.words()
# new = set([w for w in temp if w not in words])
# print(new)

# import random
# from matplotlib import pylab as plt
# def graph(text):
#     freqdist = nltk.FreqDist(text)
#     rank = 1
#     frequencies = []
#     vals = []
#     for sample, count in freqdist.most_common(500):
#         if any(c.isalpha() for c in sample):
#             frequencies.append(freqdist.freq(sample))
#             vals.append(rank)
#             rank = rank + 1
#     plt.plot(vals, frequencies)
#     plt.show()
#
# newtxt = ""
# for x in range(999999):
#     newtxt = newtxt + random.choice('abcdefg ')
# newnew = newtxt.split()
# graph(newnew)

from urllib import request
url = "https://www.worldometers.info/coronavirus/coronavirus-cases/"
response = request.urlopen(url)
raw = response.read().decode('utf8')
type(raw)
pos = raw.find("There are currently")
text = raw[pos:pos+20] + raw[pos+52:pos+75] + " of coronavirus in the world"
print(text)



