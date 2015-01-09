import json
import numpy as np
import pandas as pd
import sklearn.cluster
from pprint import pprint
import os
from makeArrayFromPrint import makearrayfromprint
json_data=open('data.txt')
import string
from collections import Counter, deque
data = json.load(json_data)
c = Counter()

STOPWORDS = {}
stopwordsfile = "stopwords.txt"
with open(stopwordsfile) as f:
    content = f.readlines()
    for val in content:
        #get rid of newline character
        val = val[:-1]

        STOPWORDS[val] = 1

def isStopword(stopwords, word):
    if stopwords.get(word,None)!=None:
        return True
    return False
def last(s):
    return s[len(s)-1]

def cleanWord(s):
    if s == "":
        return s
    if last(s) == "!" or last(s) == "?" or last(s) == "." or last(s) == "\"" or last(s) == "," or last(s) == "-":
        return cleanWord(s[:len(s)-1])
    else:
        return s

for key in data:
    line = data[key]['message'].split()
    for word in line:
        word = cleanWord(word)
        if word != "" and not isStopword(STOPWORDS,word):
            c[word]+=1
json_data.close()
print len(c)
cols = []
for key in (c):
    cols.append(key)
rmCount = 0
iterations = len(cols)
i=0
while rmCount < iterations:
    if last(cols[i]) == "!" or last(cols[i]) == "?" or last(cols[i]) == "." or last(cols[i]) == "\"" or last(cols[i]) == "," or last(cols[i]) == "-":
        cols.remove(cols[i])
    else:
        i+=1
    rmCount+=1
NUM_COLS = len(sorted(cols)) + 1
NUM_ROWS = len(data)
print "number of columns: " + str(NUM_COLS)
csvData = pd.DataFrame(data=np.zeros(shape=(NUM_ROWS,NUM_COLS)),columns=cols+["numShares!"])

messages = []
i = 0
for key in data:
    csvData["numShares!"][i] = data[key]["numShares"]
    messages.append(data[key]["message"])
    for word in (data[key]["message"]).split():
        word = cleanWord(word)
        if word != "" and not isStopword(STOPWORDS,word):
            csvData[word][i]+=1
    i+=1
y = csvData.ix[:,len(csvData.columns)-1]
data = csvData.ix[:,:len(csvData.columns)-1].as_matrix()

MS = sklearn.cluster.AffinityPropagation()
x = MS.fit_predict(data)
print "length of x: " + str(len(x))
# results from MS 
# c = makearrayfromprint("[ 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 10 0 0 0 0 7 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 14 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 11 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 13 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]")
c = x

clusters ={}
for i,val in enumerate(c):
    if val == 0:
        continue
    if clusters.get(val,None) == None:
        clusters[val] = [messages[i]]
    else:
        clusters[val].append(messages[i])

for key in clusters:
    filename = str(key) + ".txt"
    try:
        os.remove(filename)
    except OSError:
        pass
    with open(filename, 'w+') as myfile:
        for s in clusters[key]:
            myfile.write(filter(lambda x: x in string.printable, s) + "\n")


