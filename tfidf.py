import os
import json
import config
import math

os.chdir(config.res)
features = json.load(open("features.json","r"))
tfidf={"signal":{},"test":{}}

def get_idf(type):
	frequency={}
	for feature in features[type].itervalues():
		for tag in feature[3]:
			try:
				frequency[tag]+=1
			except:
				frequency[tag]=1
	D = len(features[type])
	for i in frequency.iterkeys():
		tfidf[type][tag] = math.log(0.5+D/frequency[tag])
		

get_idf("signal")
get_idf("test")

json.dump(tfidf,open("tfidf.json","w"))
