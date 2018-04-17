#!/usr/bin/python3i
# ret stores a dictionary {index:[length,noOfLiveNode,listOfIp]}
# listOfIp [local ip, dest ip 1,dest ip 2...]
import urllib.request
import re

class webScraping(object):

    def __init__(self):
        self.data = ""
        
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
            ret[x[0]]=[x[1],x[2],ip_list]
        return ret

