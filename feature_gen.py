import xml.dom.minidom as dom
import sys
import json
import os
import config
import cv2
import numpy as np
from scipy.cluster.vq import *

#from scipy.spatial.distance import cosine
data = {"signal":{},"test":{}}

xml = dom.parse(sys.argv[1])
os.chdir(config.res)
soccer100= open("soccer100.txt","r").readlines()[0].split(",")
tech100= open("tech100.txt","r").readlines()[0].split(",")
indi100= open("indi100.txt","r").readlines()[0].split(",")

soccer1000= open("soccer1000.txt","r").readlines()[0].split(",")
tech1000= open("tech1000.txt","r").readlines()[0].split(",")
indi1000= open("indi1000.txt","r").readlines()[0].split(",")

detector = cv2.FeatureDetector_create("SIFT")
descriptor = cv2.DescriptorExtractor_create("SIFT")

titles = []
# this holds number of keypoints for a given title
kp_nums = []
#holds sift kp descriptors
sift_kp_desc=[]
photos = xml.getElementsByTagName("photo")
for photo in photos:
	title = photo.getAttributeNode("id").nodeValue
	titles.append(title)
	if title in soccer100 or soccer1000:
		_class=1
	elif title in tech100 or tech1000:
		_class=2
	elif title in indi100 or indi1000:
		_class=3
	else:
		continue
	time = photo.getAttributeNode("dateTaken").nodeValue
	try:
		location = photo.getElementsByTagName("location")[0]
		lattitude = location.getAttributeNode("lattitude").nodeValue
		longitude = location.getAttributeNode("longitude").nodeValue

	except:
		lattitude = -1
		longitude = -1
	try:
		tags = [ tag.firstChild.data for tag in photo.getElementsByTagName("tag") ]
	except:
		continue

	img = cv2.imread("photos/"+title)
	skp = detector.detect(img)
	skp, sd = descriptor.compute(img, skp)
	for d in sd:
		sift_kp_desc.append(d)
	
	kp_nums.append(len(sd))

	if title in soccer100 or tech100 or indi100:
		data["signal"][title] = [time,lattitude,longitude,tags,_class]
	else:
		data["test"][title] = [time,lattitude,longitude,tags,_class]

# split into 20 clusters
res,idx = kmeans2(numpy.array(sift_kp_desc),config.SIFT_CLUSTER_SIZE)
kp_desc_index=0
for index in range(0,len(titles)):
	kp_num = kp_nums[index]
	clusters = idx[kp_desc_index:kp_desc_index+kp_num]
	kp_desc_index+ = kp_num
	if title in soccer100 or tech100 or indi100:
		data["signal"][title].append(clusters)
	else:
		data["test"][title].append(clusters)
json.dump(data,file("features.json","w"))
