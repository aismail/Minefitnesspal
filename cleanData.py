import json

def isStopword(stopwords, word):
    if stopwords.get(word.lower(),None)!=None:
        return True
    return False
def last(s):
    return s[len(s)-1]

def cleanWord(s):
    if s == "":
        return s
    if last(s) == "!" or last(s) == "?" or last(s) == "." or last(s) == "\"" or last(s) == "," or last(s) == "-":
        return cleanWord(s[:len(s)-1])
    if s[0] == '"':
        return cleanWord(s[1:])
    else:
        return s.lower()