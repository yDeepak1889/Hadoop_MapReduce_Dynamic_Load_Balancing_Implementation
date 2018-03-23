import Pyro4

HBobj = Pyro4.Proxy("PYRONAME:heartbeats")

report = {
	'host-name' : 'deepak',
	'ip' : '172.26.46.45'
}

print(HBobj.updateStatus(report))
