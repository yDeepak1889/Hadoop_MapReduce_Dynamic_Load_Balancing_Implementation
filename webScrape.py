
import urllib.request
import re

class webScraping(object):

    def __init__(self):
        self.data = ""

    def readData(self, url):

        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        self.data = resp.read()
        print(self.data)


c = webScraping()
c.readData('http://172.20.33.93:50070/fsck?ugi=hadoop&files=1&blocks=1&locations=1&path=%2Fuser%2Fhadoop%2Fbooks%2Falice.txt')

