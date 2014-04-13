import xml.dom.minidom as dom
import sys
import json
import os
import config
import datetime
from scipy.spatial.distance import cosine

os.chdir(config.res)
features = json.load(open("features.json","r"))
idf={"signal":{},"test":{}}

for feature in features["signal"].itervalues():
	for tag in feature[3]:
		try:
			idf["signal"][tag]+=1
		except:
			idf["signal"][tag]=1

for feature in features["test"].itervalues():
	for tag in feature[3]:
		try:
			idf["test"][tag]+=1
		except:
			idf["test"][tag]=1

json.dump(idf,open("idf.json","w"))
