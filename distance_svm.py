import xml.dom.minidom as dom
import sys
import json
import os
import config
import datetime
from scipy.spatial.distance import cosine
from geopy.distance import great_circle
from sklearn.svm import SVC
import  numpy as np

os.chdir(config.res)
features = json.load(open("features.json","r"))
tfidf = json.load(open("tfidf.json","r"))

def normalize(_min,_max,num):
	try:
		return (num-_min)/(_max-_min)
	except:
		print _max,_min
		exit()

def sift_vector(points):
	vector = [0]*200
	for point in points:
		vector[point]+=1
	return vector

def compute_distance(data,features1,features2,type):
	mins={"time":float("inf"),"location":float("inf"),"tag_sim":float("inf"),"sift":float("inf")}
	maxs={"time":-1,"location":-1,"tag_sim":-1,"sift":-1}
	for id1 in features1.iterkeys():
		for id2 in features2.iterkeys():
			if id1 is id2:
				continue
			time1 = datetime.datetime.strptime(features1[id1][0], "%Y-%m-%d %H:%M:%S.%f")
			time2 = datetime.datetime.strptime(features2[id2][0], "%Y-%m-%d %H:%M:%S.%f")
			time = abs((time1-time2).total_seconds())

			location1 = (features1[id1][1] ,features1[id1][2])
			location2 = (features2[id2][1] ,features2[id2][2])
			if location1 == (-1,-1) or location2 == (-1,-1):
				location = -1
			else:
				location = great_circle(location1, location2).miles
				print location1,location2,location
	
			tag_sim = 0
			for tag1 in features1[id1][3]:
				for tag2 in  features2[id2][3]:
					if tag1 == tag2:
						sim = tfidf[type][tag1]
						tag_sim+= sim*sim

			sift = cosine(sift_vector(features1[id1][5]),sift_vector(features2[id2][5]))
	
			is_same_class = 1 if features1[id1][4] == features2[id2][4] else -1

			mins["time"] = min(mins["time"],time)
			maxs["time"] = max(maxs["time"],time)
			if location is not -1:
				mins["location"] = min(mins["location"],location)
				maxs["location"] = max(maxs["location"],location)
			mins["tag_sim"] = min(mins["tag_sim"],tag_sim)
			maxs["tag_sim"] = max(maxs["tag_sim"],tag_sim)
			mins["sift"] = min(mins["sift"],sift)
			maxs["sift"] = max(maxs["sift"],sift)

			data.append([(id1,id2),[time,location,tag_sim,sift],is_same_class])

	print mins, maxs
	
	#normalize
	for index in range(0,len(data)):
		data[index][1][0] = normalize(mins["time"],maxs["time"],data[index][1][0])
		if data[index][1][1] is not -1:
			print data[index][1][1]
			data[index][1][1] = normalize(mins["location"],maxs["location"],data[index][1][1])/2
		else:
			data[index][1][1] = 1
		data[index][1][2] = normalize(mins["tag_sim"],maxs["tag_sim"],data[index][1][2])
		data[index][1][3] = normalize(mins["sift"],maxs["sift"],data[index][1][3])
		data[index][1] = np.array(data[index][1])

data_signal=[]
data_test=[]
compute_distance(data_signal,features["signal"],features["signal"],"signal")
compute_distance(data_test,features["test"],features["test"],"test")
print "distance complete"

# svm
clf = SVC()
clf.fit([data[1] for data in data_signal] , [data[2] for data in data_signal])
predicted=[]
for data in data_test:
	out = clf.predict(data[1])
	print out[0]
	predicted.append([data[0],out[0]])

json.dump({"data":predicted}, open("predicted.json","w"))
