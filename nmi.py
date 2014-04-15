import xml.dom.minidom as dom
import sys
import json
import os
import config
import cv2
import numpy as np
from sklearn.metrics.cluster import normalized_mutual_info_score as nmi
import random

#from scipy.spatial.distance import cosine
os.chdir(config.res)
soccer100= open("soccer100.txt","r").readlines()[0].split(",")
tech100= open("tech100.txt","r").readlines()[0].split(",")
indi100= open("indi100.txt","r").readlines()[0].split(",")

soccer1000= open("soccer1000.txt","r").readlines()[0].split(",")
tech1000= open("tech1000.txt","r").readlines()[0].split(",")
indi1000= open("indi1000.txt","r").readlines()[0].split(",")


data = json.load(open("results.json","r"))
data_predicted = []
data_actual = [[],[],[],[],[],[]]
combos = [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]

for id in data.iterkeys():
	data_predicted.append(data[id])
	for i in range(0,6):
		if id in soccer1000:
			data_actual[i].append(combos[i][0])
		elif id in tech1000:
			data_actual[i].append(combos[i][1])
		else:
			data_actual[i].append(combos[i][2])
test=[random.randrange(0,3)  for x in range(0,2635) ]
print nmi(data_predicted,test)
for i in range(0,6):
	print nmi(data_predicted,data_actual[i])
