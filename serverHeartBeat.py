import Pyro4
from time import time

@Pyro4.expose
class ListenHeartBeats(object):

	liveNodes = {}

	# def __init__ (self):
	# 	self.liveNodes = {}

	def updateStatus(self, data):
		required = ['host-name', 'ip']
		if not all(k in data for k in required):
			return False

		self.liveNodes[data['host-name']] = {'ip' : data['ip'], 'lastCall' : time()}

		return self.liveNodes

	def returnLiveNodes (self):
		for node in self.liveNodes.keys():
			if time() - self.liveNodes[node]['lastCall'] > 300.0 :
				self.liveNodes.pop(node, None)

		return self.liveNodes


daemon = Pyro4.Daemon()
host = '127.0.0.1' #IP address of name server
port = 5005
#host=host, port=port
ns = Pyro4.locateNS()
uri = daemon.register(ListenHeartBeats)
print("Ready. Object uri =", uri)
ns.register("heartbeats", uri)

print ("Listening . . .")
daemon.requestLoop()

