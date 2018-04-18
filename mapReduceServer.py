import pyro4
import subprocess
import os

@Pyro4.expose
class mapReduceServer():
	
	def runMapReduce(self, offset, size, inputName, outputName, runnerName): #runnerName.jar runnerName.class
		cmd = "hadoop jar "+runnerName+".jar "+runnerName+" "+offset+" "+size+" "+inputName+" "+outputName
		print(cmd)
		#returnStatus = os.system(cmd)
		return returnStatus
	

		
host = '172.20.33.93'
port = '4999'
daemon = Pyro4.Daemon(host=host, port=port)

host = '172.20.33.93'
port = '5005'

ns = Pyro4.localNS(host=host, port=port)
uri = daemon.register(mapReduceServer)
ns.register("mapReduceRunner"+ip, uri)
print("Listening . . .")
daemon.requestLoop()		
