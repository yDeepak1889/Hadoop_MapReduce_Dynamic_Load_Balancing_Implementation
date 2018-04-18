#!/usr/bin/python3i
# ret stores a dictionary {index:[length,noOfLiveNode,listOfIp]}
# listOfIp [local ip, dest ip 1,dest ip 2...]
import urllib.request
import re

class webScraping(object):

    def __init__(self):
        self.data = ""

    ''' resources{} is a map of IP's of node with the block it contains'''
    def readData(self, url):
        ret ={}
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        self.data = resp.read().decode("utf-8")
        regex = r"([0-9])\..*len=([0-9]+).*Live_repl=([0-9]+).*\]\]"
        matches = re.finditer(regex,self.data)
        for matchNum , match in enumerate(matches):
            x = match.groups()
            regex =  r"([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"
            matches_ip = re.finditer(regex,match.group())
            ip_list = []
            for ip_c,ip_s in enumerate(matches_ip):
                y = ip_s.groups()
                ip_list.append(y[0])
<<<<<<< HEAD
            ret[x[0]]=[x[1],x[2],ip_list[1:]]
        return ret



url = "http://172.20.33.93:50070/fsck?ugi=hadoop&files=1&blocks=1&locations=1&path=%2Fuser%2Fhadoop%2FS.txt"
ojb = webScraping()
print (ojb.readData(url))
=======
            ret[x[0]]=[x[1],x[2],ip_list]

        resources = {}
        for i in ret.keys():
            for ip in ret[i][2]:
                if ip not in resources and ip != '127.0.1.1' and ip!= '127.0.0.1':
                    resources[ip] = []
                if ip != '127.0.1.1' and ip!= '127.0.0.1':
                    resources[ip].append(i)

        return resources, ret


w = webScraping()
k, p  = w.readData("http://172.20.33.93:50070/fsck?ugi=hadoop&files=1&blocks=1&locations=1&path=%2Fuser%2Fhadoop%2Fbooks%2Falice.txt")
print(k)
>>>>>>> 7ac41e438c7991714036053d4cf7b2e674a860ae
