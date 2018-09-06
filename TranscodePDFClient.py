# -*- coding: utf-8 -*-
import requests, base64, os

## ****************************** url methods ************************************
url="http://127.0.0.1:8089/api/v1/file/pdf"
 
data = {"type": "url", "url": "http://47.95.219.151/firmware/resume/source/resume.html", "mandatory_parsing": True}
 
session = requests.post(url, data=data)
print(session.text)

## or

## ****************************** url methods ************************************
# source_file_path = "/Users/shilei/Desktop/jianli/html/resume.html"
# url="http://127.0.0.1:8089/api/v1/file/pdf"
 
# fileContent = open(source_file_path, 'rb').read()
# filebaseName = os.path.basename(source_file_path)
# base64Str = base64.b64encode(fileContent).decode("utf-8")
# md5Str = "c13f867a86d35f697434386985b97463"
 
# data = {"type": "content", "fileName": filebaseName, "fileContent": base64Str, "fileMD5": md5Str, "filePath": "firmware/resume/source"}
# session = requests.post(url, data=data)
# print(session.text)