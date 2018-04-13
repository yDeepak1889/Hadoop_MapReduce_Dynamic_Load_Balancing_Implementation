from resourceReportClient import *

class mainAlgorithm(object):

	def __init__(self, resources):

		self.resources = resources
		self.List_cpu = {}
		self.List_ram = {}
		self.S_node   = {}
		self.U_node   = {}
		self.P_node   = {}
		self.R_node   = {}
		self.R_hit    = {}
		self.R_cluster= 0
		self.R_max    = 0
		self.minRam   = 10000000000000000
		self.minCPU   = 10000000000000000


	def parametersCalc(self):

		'''Function calculates basic parameters which are to be used by otherParams()'''

		for i in self.resources.keys() :

			cpu = self.resources[i]['cpu']
			freq  = cpu[0]
			cores = cpu[1]


			if(cores == 1):
				P_cpu = freq
			else :
				P_cpu = freq*cores*0.8

			if P_cpu < self.minCPU:
				self.minCPU = P_cpu

			self.List_cpu[i] = P_cpu

			#Total RAM
			P_ram = self.resources[i]['ram'][0]
			self.List_ram[i] = P_ram

			if P_ram < self.minRam:
				self.minRam = P_ram

			#Storage capacity self.S_node , Used Capacity self.U_node
			S = self.resources[i]['disk'][0]
			self.S_node[i] = S

			U = self.resources[i]['disk'][1]
			self.U_node[i] = U




	#typeOfTask : 1 for memory bound, 0 for IO bound
	#gama : Lies between 0 and 1, decides the max load rate of cluster, 0.8 generally
	def otherParams(self, typeOfTask, gama):

		'''Function calculates all parameters required for main algorithm : R_hit, R_cluster, ....'''

		if(typeOfTask == 1):
			alpha = 0.8
			beta  = 0.2

		else:
			alpha = 0.2
			beta  = 0.8

		max_pBYu = -1
		U_cluster = 0
		S_cluster = 0

		for i in self.S_node.keys():

			Pi = alpha*(self.List_cpu[i]/self.minCPU) + beta*(self.List_ram[i]/self.minRam)
			self.P_node[i] = Pi

			t = Pi/self.U_node[i]

			if max_pBYu < t:
				max_pBYu = t

			Ri = (self.U_node[i]/self.S_node[i])*100
			self.R_node[i] = Ri

			U_cluster += self.U_node[i]
			S_cluster += self.S_node[i]


		self.R_cluster = (U_cluster/S_cluster)*100       #Load Ratio of the cluster
		self.R_max =  (gama + (1-gama)*self.R_cluster)*100 	#Maximum Load rate of the cluster

		#Calculating self.R_hit for each node
		for key in self.P_node.keys():

			Rhi = (self.P_node[key]/self.U_node[key])/(max_pBYu)
			self.R_hit[key] = Rhi
