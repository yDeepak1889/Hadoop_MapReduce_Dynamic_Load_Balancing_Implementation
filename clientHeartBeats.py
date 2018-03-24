import Pyro4
import socket
import time


def getIP():
	s = s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))
	return s.getsockname()[0]


def getHostName():
	return socket.gethostname()

try :
	HBobj = Pyro4.Proxy("PYRONAME:heartbeats")

except:
	print ('Something went wrong')
	


report = {
	'host-name' : getHostName(),
	'ip' : getIP()
}

while (1) :
	time.sleep(5)
	print(HBobj.updateStatus(report))
