from resourceReportClient import *
import operator
import collections

class mainAlgorithm(object):

	def __init__(self, resources, block_info):

		self.block_info = block_info
		self.resources = resources

	def parametersCalc(self):

		'''Function calculates basic parameters which are to be used by otherParams()'''
		self.List_cpu = {}
		self.List_ram = {}
		self.S_node   = {}
		self.U_node   = {}
		self.minRam   = 10000000000000000
		self.minCPU   = 10000000000000000

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
		self.P_node   = {}
		self.R_node   = {}
		self.R_hit    = {}
		self.R_cluster= 0
		self.R_max    = 0

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
			if i in self.block_info.keys():
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
			if key in self.block_info.keys():
				Rhi = (self.P_node[key]/self.U_node[key])/(max_pBYu)
				self.R_hit[key] = Rhi


	def alloc(self, no_of_blocks):
		'''Function allocates the mapper and reducer tasks to the blocks according to R_hit values'''

		count = 0
		allocated = []
		final = []

		while count < no_of_blocks:
			Nodes1 = {}
			Nodes2 = {}
			Nodes3 = {}
			result = []

			flag = 0
			for i in self.R_hit.keys():

				if(self.R_hit[i] <= self.R_cluster):
					Nodes1[i] = self.R_hit[i]

				elif(self.R_hit[i] > self.R_cluster and self.R_hit[i] < self.R_max):
					Nodes2[i] = self.R_hit[i]

				else:
					Nodes3[i] = self.R_hit[i]

			print(Nodes1)
			if Nodes1:
				Nodes1 = collections.OrderedDict(sorted(Nodes1.items(), key=lambda t: t[1], reverse = True))
				#print("____________________",Nodes1)
				for key in Nodes1.keys():
					if self.block_info[key]:
						for block in self.block_info[key]:
							if block[0] not in allocated:
								result.append(block[0])
								result.append(key)
								result.append(block[1])
								allocated.append(block[0])
								count += 1
								flag = 1
								break
						if flag==1:
							break

			elif Nodes2 and flag != 1:
				Nodes2 = collections.OrderedDict(sorted(Nodes2.items(), key=lambda t: t[1], reverse = True))
				for key in Nodes2.keys():
					if self.block_info[key]:
						for block in self.block_info[key]:
							if block[0] not in allocated:
								result.append(block[0])
								result.append(key)
								result.append(block[1])
								allocated.append(block[0])
								flag1 =1
								count+=1
								break
						if flag1 == 1:
							break
			
	
			final.append(result)

			'''result[] has the IP and the block stored that is currently allocated, do whatever you want with that'''
			if count < no_of_blocks:
				self.parametersCalc()
				self.otherParams(1, 0.8)


		return final

