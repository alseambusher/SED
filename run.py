import xml.dom.minidom as dom
import sys
import json
import os
import config
import datetime
from scipy.spatial.distance import cosine
from geopy.distance import great_circle
from sklearn.svm import SVC

os.chdir(config.res)
soccer100= open("soccer100.txt","r").readlines()[0].split(",")
tech100=open("tech100.txt","r").readlines()[0].split(",")
indi100=open("indi100.txt","r").readlines()[0].split(",")

soccer1000= open("soccer1000.txt","r").readlines()[0].split(",")
tech1000=open("tech1000.txt","r").readlines()[0].split(",")
indi1000=open("indi1000.txt","r").readlines()[0].split(",")

features = json.load(open("features.json","r"))
tfidf = json.load(open("tfidf.json","r"))

def normalize(_min,_max,num):
	return (num-_min)/(_max-_min)

def compute_distance(data,features1,features2):
	mins={"time":float("inf"),"location":float("inf"),"tag_sim":float("inf"),"sift":float("inf")}
	maxs={"time":-1,"location":-1,"tag_sim":-1,"sift":-1}
	for id1 in features1.iterkeys():
		for id2 in features2.iterkeys():
			time1 = datetime.datetime.strptime(features1[id1][0], "%Y-%m-%d %H:%M:%S.%f")
			time2 = datetime.datetime.strptime(features2[id2][0], "%Y-%m-%d %H:%M:%S.%f")
			time = abs((time1-time2).total_seconds())

			location1 = (features1[id1][1] ,features1[id1][2])
			location2 = (features2[id2][1] ,features2[id2][2])
			if location1 is (-1,-1) or location2 is (-1,-1):
				location = -1
			else:
				location = great_circle(location1, location2).miles
	
			tag_sim = 0
			for tag1 in features1[id1][3]:
				for tag2 in  features2[id2][3]:
					if tag1 == tag2:
						sim = tfidf["signal"][tag1]
						tag_sim+= sim*sim

			sift = cosine(features1[id1][5],features2[id2][5])
	
			is_same_class = 1 if features1[id1][4] == features2[id2][4] else 0

			mins["time"] = min(mins["time"],time)
			maxs["time"] = max(mins["time"],time)
			if location is not -1:
				mins["location"] = min(mins["location"],location)
				maxs["location"] = max(mins["location"],location)
			mins["tag_sim"] = min(mins["tag_sim"],tag_sim)
			maxs["tag_sim"] = max(mins["tag_sim"],tag_sim)
			mins["sift"] = min(mins["sift"],sift)
			maxs["sift"] = max(mins["sift"],sift)

			data.append(((id1,id2),[time,location,tag_sim,sift],is_same_class))
	
	#normalize
	for index in range(0,len(data)):
		data[index][1][0] = normalize(mins["time"],max["time"],data[index][1][0])
		if data[index][1][1] is not -1:
			data[index][1][1] = normalize(mins["location"],max["location"],data[index][1][1])/2
		else:
			data[index][1][1] = 1
		data[index][1][2] = normalize(mins["tag_sim"],max["tag_sim"],data[index][1][2])
		data[index][1][3] = normalize(mins["sift"],max["sift"],data[index][1][3])
		data[index][1] = np.array(data[index][1])

data_signal=[]
data_test=[]
compute_distance(data_signal,features["signal"],features["signal"])
compute_distance(data_test,features["test"],features["signal"])
print "distance complete"

# svm
clf = SVC()
clf.fit([data[1] for data in data_signal] , [data[2] for data in data_signal])
predicted=[]
for data in data_test:
	predicted.append([data[1],clf.predict(data[1]))

json.dump({"data":predicted}, open("predicted.json","w"))
