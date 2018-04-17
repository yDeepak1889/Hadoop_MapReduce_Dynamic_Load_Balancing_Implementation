
import urllib.request
import re

class webScraping(object):

    def __init__(self):
        self.data = ""
        
    def readData(self, url):

        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        self.data = resp.read().decode("utf-8") 
        regex = r"([0-9])\..*len=([0-9]+).*Live_repl=([0-9]+).*Storage\[([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*\]\]"
        matches = re.finditer(regex,self.data)
        for matchNum , match in enumerate(matches):
            matchNum = matchNum + 1
            print(match.group())
            for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1
                        print(match.group(groupNum))
c = webScraping()
c.readData('http://172.20.33.93:50070/fsck?ugi=hadoop&files=1&blocks=1&locations=1&path=%2Fuser%2Fhadoop%2Fbooks%2Falice.txt')



