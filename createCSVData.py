import json
import numpy as np
import pandas as pd
from pprint import pprint
json_data=open('data.txt')
from collections import Counter, deque
data = json.load(json_data)
c = Counter()

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
        c[word]+=1
json_data.close()

cols = []
for key in (c):
    cols.append(key)
print len(cols)
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

csvData = pd.DataFrame(data=np.zeros(shape=(NUM_ROWS,NUM_COLS)),columns=cols+["numShares!"])

i = 0
print "got here"
for key in data:
    csvData["numShares!"][i] = data[key]["numShares"]
    for word in data[key]["message"]:
        word = cleanWord(word)
        if word != "":
            print word
            print key
            csvData[word][i]+=1
    i+=1

