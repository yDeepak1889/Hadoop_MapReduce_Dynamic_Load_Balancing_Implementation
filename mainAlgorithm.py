from resourceReportClient import *

resources = {}
resources = getResourceStatusOfDataNodes()



List_cpu = {}
List_ram = {}
S_node   = {}
U_node   = {}
P_node   = {}
R_node   = {}
R_hit    = {}
R_cluster= 0
R_max    = 0

minRam   = 10000000000000
minCPU   = 10000000000000


def parametersCalc():

	global minRam
	global minCPU

	for i in resources.keys() :

		cpu = resources[i]['cpu']
		freq  = cpu[0]
		cores = cpu[1]

	
		if(cores == 1):
			P_cpu = freq
		else :
			P_cpu = freq*cores*0.8 

		if P_cpu < minCPU:
			minCPU = P_cpu

		List_cpu[i] = P_cpu

		#Total RAM
		P_ram = resources[i]['ram'][0]
		List_ram[i] = P_ram

		if P_ram < minRam:
			minRam = P_ram

		#Storage capacity S_node , Used Capacity U_node
		S = resources[i]['disk'][0]
		S_node[i] = S

		U = resources[i]['disk'][1]
		U_node[i] = U




#typeOfTask : 1 for memory bound, 0 for IO bound
#gama : Lies between 0 and 1, decides the max load rate of cluster, 0.8 generally

def otherParams(typeOfTask, gama):
	
	if(typeOfTask == 1):
		alpha = 0.8
		beta  = 0.2

	else:
		alpha = 0.2
		beta  = 0.8

	max_pBYu = -1
	U_cluster = 0
	S_cluster = 0

	global R_cluster
	global R_max

	for i in S_node.keys():

		Pi = alpha*(List_cpu[i]/minCPU) + beta*(List_ram[i]/minRam)
		P_node[i] = Pi

		t = Pi/U_node[i]

		if max_pBYu < t:
			max_pBYu = t

		Ri = (U_node[i]/S_node[i])*100
		R_node[i] = Ri

		U_cluster += U_node[i]
		S_cluster += S_node[i]


	R_cluster = (U_cluster/S_cluster)*100       #Load Ratio of the cluster
	R_max =  (gama + (1-gama)*R_cluster)*100 	#Maximum Load rate of the cluster


	#Calculating R_hit for each node

	for key in P_node.keys():

		Rhi = (P_node[key]/U_node[key])/(max_pBYu)
		R_hit[key] = Rhi


parametersCalc()
otherParams(1, 0.8)


