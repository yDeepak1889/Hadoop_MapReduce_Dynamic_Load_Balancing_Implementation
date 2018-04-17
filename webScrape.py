
import urllib.request
import re

url = 'http://172.20.33.93:50070/fsck?ugi=hadoop&files=1&blocks=1&locations=1&path=%2Fuser%2Fhadoop%2Fbooks%2Falice.txt'

req = urllib.request.Request(url)
resp = urllib.request.urlopen(req)
respData = resp.read()
print(str(respData))
