import json
import os
import config
import  numpy as np
from scipy.cluster.vq import *

os.chdir(config.res)

features = json.load(open("features.json","r"))
predicted = json.load(open("predicted.json","r"))["data"]
signal_ids = features["signal"].keys()
ids = [ item[0][0] for item in predicted ]
#initialize array
vectors = [[0]*len(signal_ids)]*len(predicted)

for item in predicted:
	signal_index = signal_ids.index(item[0][1])
	id_index = ids.index(item[0][0])
	vectors[id_index][signal_index] = item[1]
res,idx = kmeans2(np.array(vectors),3)
idx = list(idx)

result = {}
for id_index in range(0,len(ids)):
	result[ids[id_index]] = idx[id_index]

json.dump(result,open("results.json","w"))

	
