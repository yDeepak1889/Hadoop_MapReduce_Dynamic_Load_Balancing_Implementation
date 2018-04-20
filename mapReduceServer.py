import pyro4
import subprocess
import os
import socket

def getIP():
	s = s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))
	return s.getsockname()[0]

@Pyro4.expose
class mapReduceServer():
	
	def runMapReduce(self, offset, size, inputName, outputName, mapperName): #runnerName.jar runnerName.class
		cmd = "hadoop jar "+mapperName+".jar "+mapperName+" "+offset+" "+size+" "+inputName+" "+outputName
		print(cmd)
		#returnStatus = os.system(cmd)
		return returnStatus
	

		
host = '172.20.33.72'
port = '4999'
daemon = Pyro4.Daemon(host=host, port=port)

host = '172.20.33.93'
port = '5005'

ip = getIP()

ns = Pyro4.localNS(host=host, port=port)
uri = daemon.register(mapReduceServer)
ns.register("mapReduceRunner"+ip, uri)
print("Listening . . .")
daemon.requestLoop()		
