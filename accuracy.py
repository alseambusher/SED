import xml.dom.minidom as dom
import sys
import json
import os
import config
import cv2
import numpy as np
from sklearn.metrics import mutual_info_score as nmi
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
data_actual = []
#combos = [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]
match = 0
matched = [0,0,0]
wrong = [0,0,0]

for id in data.iterkeys():
	data_predicted.append(data[id])
	if id in soccer1000:
		data_actual.append(0)
		if data[id] == 0:
			match+=1
			matched[0]+=1
		else:
			wrong[0]+=1
	elif id in tech1000:
		data_actual.append(2)
		if data[id] == 2:
			match+=1
			matched[2]+=1
		else:
			wrong[2]+=1
	else:
		data_actual.append(1)
		if data[id] == 1:
			match+=1
			matched[1]+=1
		else:
			wrong[1]+=1

print match
print matched
print wrong
#print nmi(data_predicted,data_actual)
