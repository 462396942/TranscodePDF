# -*- coding: utf-8 -*-
import requests, os
import socket
import re

def getIP(domain):
	myaddr = socket.getaddrinfo(domain, 'http')
	return myaddr[0][4][0]

def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False

def upload(url=None, target_file_path=None, path=None):

	domain = url.split("/")[2].split(":")[0]
	domain_ip = ""
	if not isIP(domain):
		domain_ip = getIP(domain)
		url = url.replace(domain, domain_ip)

	fileName = os.path.basename(target_file_path)
	files = {"file1": (fileName, open(target_file_path, 'rb'), "multipart/form-data")}

	data = {"custom_path": path}
	session = requests.post(url, data=data, files=files)
	# print("session:", session)
	return session.text