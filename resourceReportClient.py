import Pyro4
import socket


def getResourceStatusOfDataNodes() :
	result = {}

	try :
		HBobj = Pyro4.Proxy("PYRONAME:heartbeats")

	except:
		print ('Something went wrong')
		return result

	datanodeInfo = HBobj.returnLiveNodes()

	for dataNode in datanodeInfo.keys():
		HBobj = Pyro4.Proxy("PYRONAME:monitorModule" +datanodeInfo[dataNode]['ip'])
		result[datanodeInfo[dataNode]['ip']]['cpu'] = HBobj.getCPUinfo()
		result[datanodeInfo[dataNode]['ip']]['ram'] = HBobj.getRAMinfo()
		result[datanodeInfo[dataNode]['ip']]['disk'] = HBobj.getDISKinfo()

	return result

