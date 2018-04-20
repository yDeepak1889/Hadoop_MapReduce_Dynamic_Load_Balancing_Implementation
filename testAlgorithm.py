from mainAlgorithm import *
from webScrape import *
from resourceReportClient import *

w = webScraping()
block_info, no_of_blocks = w.readData("http://172.20.33.93:50070/fsck?ugi=hadoop&blocks=1&locations=1&files=1&path=%2Fuser%2Fhadoop%2FS.txt")
#print(k)

resources = {}
resources = getResourceStatusOfDataNodes()
implement = mainAlgorithm(resources, block_info)
implement.parametersCalc()
implement.otherParams(1, 0.8)
final = []
final = implement.alloc(no_of_blocks)

for i in final:
	print(i)
