import xml.dom.minidom as dom
import sys
import json
import os
import config
import cv2
import numpy as np
from scipy.cluster.vq import *

#from scipy.spatial.distance import cosine
os.chdir(config.res)
soccer100= open("soccer100.txt","r").readlines()[0].split(",")
tech100= open("tech100.txt","r").readlines()[0].split(",")
indi100= open("indi100.txt","r").readlines()[0].split(",")

soccer1000= open("soccer1000.txt","r").readlines()[0].split(",")
tech1000= open("tech1000.txt","r").readlines()[0].split(",")
indi1000= open("indi1000.txt","r").readlines()[0].split(",")

detector = cv2.SIFT()

data = json.load(open("features.json","r"))
titles = []
# this holds number of keypoints for a given title
kp_nums = []
#holds sift kp descriptors
sift_kp_desc=[]
def compute_sift(type):
	for photo in data[type].iterkeys():
		title=photo
		titles.append(title)
	
		img = cv2.imread("photos/"+title+".jpg")
		skp = detector.detect(img)
		skp, sd = detector.compute(img, skp)
		for d in sd:
			sift_kp_desc.append(d)
	
		kp_nums.append(len(sd))

compute_sift("signal")
compute_sift("test")
# split into 20 clusters
res,idx = kmeans2(numpy.array(sift_kp_desc),config.SIFT_CLUSTER_SIZE)
kp_desc_index=0
for index in range(0,len(titles)):
	kp_num = kp_nums[index]
	clusters = idx[kp_desc_index:kp_desc_index+kp_num]
	kp_desc_index+= kp_num
	if title in soccer100 or tech100 or indi100:
		data["signal"][title].append(clusters)
	else:
		data["test"][title].append(clusters)
json.dump(data,file("features.json","w"))
