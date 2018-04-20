import Pyro4
import subprocess
import os
import sys
from mainAlgorithm import *
from webScrape import *
from resourceReportClient import *


def mapperClient (ip, inputName, offset, size, outputName, MapperName):
	try :
		HBobj = Pyro4.Proxy("PYRONAME:mapReduceRunner"+ip)
	except:
		print ('Something went wrong:(')
	
	
	HBobj.initJob(mapperName)
	
	status = HBobj.runMapReduce(offset, size, inputName, outputName, MapperName)
	return status


def reducerClient(ip, outputName, reducerName, count):
	try :
		HBobj = Pyro4.Proxy("PYRONAME:mapReduceRunner"+ip)
	except:
		print ('Something went wrong:(')
	
	cmd = "javac " + reducerName +".java "+"-cp $(../hadoop/sbin/hadoop classpath)"
	os.system(cmd)
	
	cmd = "jar cvf " + reducerName +".jar " + reducerName+".class"
	os.system(cmd)
	
	cmd = "hdfs dfs -put " + reducerName + ".jar"
	os.system(cmd)
	
	cmd = "hdfs dfs -put " + reducerName + ".class"
	os.system(cmd)
	
	HBobj.initJob(reducerName)
	status = HBobj.runReduceTask(outputName, outputName+".txt", reducerName, count)
	
	return status



if __name__=="__main__":
	params = sys.argv
	
	inputName = params[3]
	mapperName = params[1]
	reducerName = params[2]
	output = params[4]
	
	fileName = "http://172.20.33.93:50070/fsck?ugi=hadoop&blocks=1&locations=1&files=1&path=%2Fuser%2Fhadoop%2FtestFile.txt"
	
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
	
	print ("Initializing job...")
	
	cmd = "javac " + mapperName+".java "+"-cp $(../hadoop/sbin/hadoop classpath)"
	os.system(cmd)
	
	cmd = "jar cvf " + mapperName+".jar " + mapperName+".class"
	os.system(cmd)
	
	cmd = "hdfs dfs -put " + mapperName + ".jar"
	os.system(cmd)
	
	cmd = "hdfs dfs -put " + mapperName + ".class"
	os.system(cmd)
	
	print ("Initialization Done.")
	
	count = len(final)
	
	for i in final:
		print("Running Mapper", i,"...")
		while (mapperClient(i[1], inputName, str(offset), i[2], output+i[0]+".txt", mapperName) != 0):
			pass
		
		offset = offset + int(i[2])
		print("Mapper", i, "completed")
	
	while (reducerClient(i[1], output, reducerName, str(count)) != 0) :
		pass
	
	print ("Job completed! :)")
	
	
