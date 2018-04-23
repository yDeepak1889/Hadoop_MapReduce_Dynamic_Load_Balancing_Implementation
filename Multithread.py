import threading


def print_square(number):
	print(number*number)


class thread(object):

	def createThreads(self, no_of_tasks):

		listOfThreads = []

		for i in range(0, no_of_tasks):
			t = threading.Thread(target=print_square, args=(i+1,))
			listOfThreads.append(t)
			t.start()

		for i in listOfThreads:
			i.join()

		print("Success")


t = thread()
t.createThreads(20)
