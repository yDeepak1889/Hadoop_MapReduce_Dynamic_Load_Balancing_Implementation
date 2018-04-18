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


host = '172.20.33.93' #Own IP address
port = 5001
daemon = Pyro4.Daemon(host=host, port=port)
#host=host, port=port
port = 5005
ns = Pyro4.locateNS(host=host, port=port)
uri = daemon.register(ListenHeartBeats)
print("Ready. Object uri =", uri)
ns.register("heartbeats", uri)

print ("Listening . . .")
daemon.requestLoop()
