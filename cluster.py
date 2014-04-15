import json
import os
import config
import  numpy as np
from scipy.cluster.vq import *
import threading

os.chdir(config.res)

features = json.load(open("features.json","r"))
predicted = json.load(open("predicted.json","r"))["data"]
signal_ids = features["signal"].keys()
ids = [ item[0][0] for item in predicted ]
#initialize array
#vectors = [[0]*len(signal_ids)]*len(predicted)
vectors = []
a=0
for id_index in range(0,len(ids)):
	vector = []
	for item in predicted[id_index*len(signal_ids):(id_index+1)*len(signal_ids)]:
		vector.append(item[1])
	vectors.append(vector)
"""
def gen_vector(begin,end):
	for item in predicted[begin:end]:
		signal_index = signal_ids.index(item[0][1])
		id_index = ids.index(item[0][0])
		vectors[id_index][signal_index] = item[1]
start=0
num_threads=50
block_size=len(predicted)/num_threads
threads = []
for i in range(0,num_threads):
	print i
	thread = threading.Thread(target=gen_vector,args=(start,start+block_size))
	thread.start()
	start+=block_size
"""
print "vectors generated"

res,idx = kmeans2(np.array(vectors),3)
idx = list(idx)

result = {}
for id_index in range(0,len(ids)):
	result[ids[id_index]] = idx[id_index]

json.dump(result,open("results.json","w"))

	
