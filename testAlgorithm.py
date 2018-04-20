from mainAlgorithm import *
from webScrape import *
from resourceReportClient import *

w = webScraping()
k = w.readData("http://172.20.33.93:50070/fsck?ugi=hadoop&blocks=1&locations=1&files=1&path=%2Fuser%2Fhadoop%2FS.txt")
#print(k)

resources = {}
resources = getResourceStatusOfDataNodes()
implement = mainAlgorithm(resources, k)
implement.parametersCalc()
implement.otherParams(1, 0.8)
final = []
final = implement.alloc(5)

for i in final:
	print(i)
