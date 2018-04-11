import Pyro4
import psutil
import socket


def getIP():
	s = s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))
	return s.getsockname()[0]


@Pyro4.expose
class monitorSystem(object):
	
	def getCPUinfo(self):
		cpuFreq = psutil.cpu_freq(percpu=True)
		core = len(cpuFreq)
		totalCPUFreq = 0
		
		for freq in cpuFreq:
			totalCPUFreq += freq[0]
	
		return (totalCPUFreq, core)


	def getRAMinfo(self):
		RAM = psutil.virtual_memory()
		return (RAM[0], RAM[1]) # (total ram, available ram) 


	def getDISKinfo(self):
		diskSpace = psutil.disk_usage('/')
		return (diskSpace[0], diskSpace[1]) # (total space, used space)


daemon = Pyro4.Daemon()
host = '127.0.0.1' #IP address of name server
port = 5005
#host=host, port=port
ns = Pyro4.locateNS()
uri = daemon.register(monitorSystem)
ns.register("monitorModule" + getIP(), uri)

print ("Listening . . .")
daemon.requestLoop()
	