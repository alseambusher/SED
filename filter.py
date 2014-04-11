import os
os.chdir("../res")
all = open("photos.txt","r")
soccer = open("soccer_events.txt","r")
tech = open("technical_events.txt", "r")
indi =open("indignados_events.txt","r")
all_array = all.readlines()[0].split(",")
soccer_array = soccer.readlines()[0].split(",")
tech_array= tech.readlines()[0].split(",")
indi_array =indi.readlines()[0].split(",")

def get_array(array,num):
	result = [sub if sub in array else None for sub in all_array]
	result = [ x for x in result if x is not None ]
	return ",".join(result[:num])

soccer100 = get_array(soccer_array,100)
tech100 = get_array(tech_array,100)
indi100 = get_array(indi_array,100)

soccer1000 = get_array(soccer_array,1000)
tech1000 = get_array(tech_array,1000)
indi1000 = get_array(indi_array,1000)

soccer100_file=open("soccer100.txt","w")
tech100_file=open("tech100.txt","w")
indi100_file=open("indi100.txt","w")

soccer1000_file=open("soccer1000.txt","w")
tech1000_file=open("tech1000.txt","w")
indi1000_file=open("indi1000.txt","w")

soccer100_file.write(soccer100)
tech100_file.write(tech100)
indi100_file.write(indi100)

soccer1000_file.write(soccer1000)
tech1000_file.write(tech1000)
indi1000_file.write(indi1000)
