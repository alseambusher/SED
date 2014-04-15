import json
import os
import config
import  numpy as np
from scipy.cluster.vq import *
from sklearn.cluster import KMeans
import threading

os.chdir(config.res)

features = json.load(open("features.json","r"))
predicted = json.load(open("predicted.json","r"))["data"]
#signal_ids = features["signal"].keys()
ids = list(set([ item[0][0] for item in predicted ]))
#initialize array
#vectors = [[0]*len(signal_ids)]*len(predicted)
vectors = []
a=0
for id_index in range(0,len(ids)):
	vector = []
	for item in predicted[id_index*len(ids):(id_index+1)*len(ids)-1]:
		vector.append(item[1])
	vector.insert(id_index,1)
	vectors.append(vector)
print "vectors generated"

#res,idx = kmeans(np.array(vectors),3)
#print res,idx
#idx = list(idx)
kmeans = KMeans(3)
idx = list(kmeans.fit(vectors).labels_)

result = {}
for id_index in range(0,len(ids)):
	result[ids[id_index]] = idx[id_index]

json.dump(result,open("results.json","w"))
