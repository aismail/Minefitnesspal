import json
import numpy as np
import pandas as pd
from pprint import pprint
json_data=open('data.txt')
from collections import Counter
data = json.load(json_data)
c = Counter()

np.zeros(shape=(2,4))

for key in data:
  line = data[key]['message'].split()
  for word in line:
    c[word]+=1
json_data.close()


print
