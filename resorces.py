from webScrape import *

class Resources(object):

    def __init__(self):
        pass

    def getBlockInfo(self, url):
        resources = {}
        w = webScraping()
        block_data = w.readData(url)

        for i in block_data.keys():
            for ip in block_data[i][2]:
                if ip not in resources and ip != '127.0.1.1' and ip!= '127.0.0.1':
                    resources[ip] = []
                if ip != '127.0.1.1' and ip!= '127.0.0.1':
                    resources[ip].append(i)

        return resources










r = Resources()
r.getBlockInfo("http://172.20.33.93:50070/fsck?ugi=hadoop&files=1&blocks=1&locations=1&path=%2Fuser%2Fhadoop%2Fbooks%2Falice.txt")
