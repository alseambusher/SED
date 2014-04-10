import xml.dom.minidom as dom
import sys
import json
#import signal

data = {}
images = []
#def save_json(signal,frame):
	#json.dump(data,file("features.json","w"))	
	#exit(0)
#signal.signal(signal.SIGINT,save_json)

xml = dom.parse(sys.argv[1])
photos = xml.getElementsByTagName("photo")
for photo in photos:
	#title = photo.getElementsByTagName("title")[0].firstChild.data
	#title = title.split(" ")[0] # get only the first part
	title = photo.getAttributeNode("id").nodeValue
	if title not in images:
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
		tags = [ tag.firstChild.data in for tag in photo.getElementsByTagName("tag") ]
	except:
		continue
	data[title] = [time,lattitude,longitude,tags]
	#sift
json.dump(data,file("features.json","w"))	
