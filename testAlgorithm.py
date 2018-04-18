from mainAlgorithm import *
from webScrape import *
from resourceReportClient import *

w = webScraping()
k, p  = w.readData("http://172.20.33.93:50070/fsck?ugi=hadoop&files=1&blocks=1&locations=1&path=%2Fuser%2Fhadoop%2Fbooks%2Falice.txt")
print(k)

resources = {}
resources = getResourceStatusOfDataNodes()
implement = mainAlgorithm(resources, k)
implement.parametersCalc()
implement.otherParams(1, 0.8)
print(implement.R_hit)



implement.alloc()
