import Pyro4
import socket

def getIP():
	s = s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))
	return s.getsockname()[0]


def getHostName():
	return socket.gethostname()

HBobj = Pyro4.Proxy("PYRONAME:heartbeats")

report = {
	'host-name' : getHostName(),
	'ip' : getIP()
}

print(HBobj.updateStatus(report))
