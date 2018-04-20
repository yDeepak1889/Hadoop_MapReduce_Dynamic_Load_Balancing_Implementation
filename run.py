import Pyro4
import subprocess
import os
from mainAlgorithm import *
from webScrape import *
from resourceReportClient import *


def mapReduceClient (ip, inputFile, offset, size, outputFile, MapperName):
	try :
		HBobj = Pyro4.Proxy("PYRONAME:mapReduceRunner"+ip)
	except:
		print ('Something went wrong:(')
	
	status = HBobj.runMapReduce(offset, size, inputName, outputName, MapperName)
	return status
	

if __name__=="__main__":
	
	fileName = "http://172.20.33.93:50070/fsck?ugi=hadoop&blocks=1&locations=1&files=1&path=%2Fuser%2Fhadoop%2FS.txt"
	
	w = webScraping()
	block_info, no_of_blocks = w.readData(fileName)
	
	resources = {}
	resources = getResourceStatusOfDataNodes()
	implement = mainAlgorithm(resources, block_info)
	implement.parametersCalc()
	implement.otherParams(1, 0.8)
	final = []
	final = implement.alloc(no_of_blocks)
	
	offset = 0
	
	for i in final:
		mapReduceClient(i[1], inputName, offset, i[2], output+i[0]+".txt", mapperName)
		offset = offset + int(i[2])
	
	
