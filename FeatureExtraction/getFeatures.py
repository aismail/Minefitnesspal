import json
from collections import Counter
import sys
sys.path.insert(0, '..')
from cleanData import cleanWord, last, isStopword
from operator import itemgetter


json_data=open('../data.txt')
data = json.load(json_data)
c = Counter()
STOPWORDS = {}
stopwordsfile = "../stopwords.txt"
with open(stopwordsfile) as f:
    content = f.readlines()
    for val in content:
        #get rid of newline character
        val = val[:-1]
        STOPWORDS[val] = 1
dataList = []
i = 0
for key in data:
    dataList.append(data[key])
    dataList[i]['id'] = key
    i+=1

dataList.sort(key = itemgetter('numShares'), reverse = True)

topratio = 0.2
dataList = dataList[:int( topratio * float(len(dataList)))]

best_words = Counter()
print len(dataList)
for i,val in enumerate(dataList):
    for word in (val["message"]).split():
        word = cleanWord(word)
        if word != "" and not isStopword(STOPWORDS,word):
            best_words[word] +=1
print len(best_words)





json_data.close()