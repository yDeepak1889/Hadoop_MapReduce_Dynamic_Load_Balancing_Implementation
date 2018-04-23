import Pyro4
import subprocess
import os
import sys
from webScrape import *
from resourceReportClient import *


def mapperClient (ip, inputName, offset, size, outputName, mapperName):
	try :
		HBobj = Pyro4.Proxy("PYRONAME:mapReduceRunner"+ip)
	except:
		print ('Something went wrong:(')


	HBobj.initJob(mapperName)

	status = HBobj.runMapReduce(offset, size, inputName, outputName, mapperName)
	return status


def reducerClient (ip, outputName, reducerName, count):
	try :
		HBobj = Pyro4.Proxy("PYRONAME:mapReduceRunner"+ip)
	except:
		print ('Something went wrong:(')

	print ("Running Reducer Task...")
	cmd = "javac " + reducerName +".java "+"-cp $(../hadoop/bin/hadoop classpath)"
	os.system(cmd)

	cmd = "jar cvf " + reducerName +".jar " + reducerName+".class"
	os.system(cmd)

	cmd = "hdfs dfs -put " + reducerName + ".jar"
	os.system(cmd)

	cmd = "hdfs dfs -put " + reducerName + ".class"
	os.system(cmd)

	HBobj.initJob(reducerName)
	status = HBobj.runReduceTask(outputName, outputName+".txt", reducerName, count)
	print ("Reducer Task Completed")
	return status

def initJob (mapperName):
	print ("Initializing job...")

	cmd = "javac " + mapperName+".java "+"-cp $(../hadoop/bin/hadoop classpath)"
	os.system(cmd)

	cmd = "jar cvf " + mapperName+".jar " + mapperName+".class"
	os.system(cmd)

	cmd = "hdfs dfs -put " + mapperName + ".jar"
	os.system(cmd)

	cmd = "hdfs dfs -put " + mapperName + ".class"
	os.system(cmd)

	print ("Initialization Done.")

# if __name__=="__main__":
# 	offset = 0
#
# 	count = len(final)
#
# 	for i in final:
# 		print("Running Mapper", i,"...")
# 		while (mapperClient(i[1], inputName, str(offset), i[2], output+i[0]+".txt", mapperName) != 0):
# 			pass
#
# 		offset = offset + int(i[2])
# 		print("Mapper", i, "completed")
#
# 	while (reducerClient(i[1], output, reducerName, str(count)) != 0) :
# 		pass
#
# 	print ("Job completed! :)")
