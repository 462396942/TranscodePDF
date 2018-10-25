#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from django import conf
from ConvertFileFormat.controller.pdf import main
import os, time, requests, json, datetime, re, shutil, urllib, uuid, base64
from django.utils.safestring import mark_safe
from ExportWord import export

def GetFileAPI(request):
	ret = {
		"apis":[
			{
				"path": "/api/v1/file/pdf",
				"description": "Process files into PDF format."
			},
			{
				"path": "/api/v1/file/word",
				"description": "Receive word template and data, write data to word template back word."
			},
		]
	}
	if request.method == "GET":
		return JsonResponse(ret)
	ret = {"status": "failed", "status_code": "503", "description": "Illegal access without using a request type other than GET."}
	return JsonResponse(ret)

def GeneratePDF(request):

	ret = {
		"apis":[
			{	
				"type": "POST",
				"format": "JSON",
				"description": "Process files into PDF format.",
				"parameter1": {
					"type": "url",
					"url": "...",
					"mandatory_parsing": "False (Not necessary)",
					"filePath": "../../.. (Not necessary)"
				},
				"parameter2": {
					"fileMD5": "... (Not necessary)",
					"type": "content",
					"fileName": "...",
					"fileContent": "base64Str",
					"filePath": "../../.."
				},
			}
		]
	}
	_emptyData = []
	if request.method == "GET":
		return JsonResponse(ret)
	elif request.method == "POST":

		# Initialization Data
		ReceiveData = request.POST
		transportType = ReceiveData["type"] if "type" in ReceiveData else ""
		
		if transportType == "content":
			fileName = ReceiveData["fileName"] if "fileName" in ReceiveData else _emptyData.append("fileName")
			fileContent = ReceiveData["fileContent"] if "fileContent" in ReceiveData else _emptyData.append("fileContent")
			fileMD5 = ReceiveData["fileMD5"] if "fileMD5" in ReceiveData else ""
			filePath = ReceiveData["filePath"] if "filePath" in ReceiveData else _emptyData.append("filePath")
		elif transportType == "url":
			_url = ReceiveData["url"] if "url" in ReceiveData else _emptyData.append("url")
			mp = ReceiveData["mandatory_parsing"] if "mandatory_parsing" in ReceiveData else "False"
			mp = True if mp == "True" else False
			filePath = ReceiveData["filePath"] if "filePath" in ReceiveData else ""
		else:
			ret = {"status": "failed", "status_code": "503", "description": "Incorrect transfer, specify the correct 'type' is 'content or url'."}
			return JsonResponse(ret)

		# Determine whether there is free data
		if _emptyData:
			ret = {"status": "failed", "status_code": "503", "description": "Lack of necessary data '{}'.".format(", ".join(_emptyData))}
			return JsonResponse(ret)

		# Run main
		if transportType == "content":
			ret = main(
				transport_type=transportType, 
				fileName=fileName, 
				fileContent=fileContent, 
				fileMD5=fileMD5,
				filePath=filePath,
			)
		elif transportType == "url":
			ret = main(
				transport_type=transportType, 
				url=_url,
				mp=mp,
				filePath=filePath,
			)
	return JsonResponse(ret)


def GenerateWord(request):

	ret = {
		"apis":[
			{	
				"type": "POST",
				"format": "JSON",
				"description": "Receive word template and data, write data to word template back word.",
				"parameter1": {
					"type": "url",
					"url": "...",
					"data": "<ResumeCandidateInfo>",
				},
				"parameter2": {
					"type": "file",
					"fileContent": "(Base64<ResumeTemplate>)",
					"data": "<ResumeCandidateInfo>",
				},
			}
		]
	}
	if request.method == "GET":
		return JsonResponse(ret)
	elif request.method == "POST":
		
		# Initialization Data
		ReceiveData = request.POST
		transportType = ReceiveData["type"] if "type" in ReceiveData else ""
		if ReceiveData["data"] == list:
			ResumeCandidateInfo = json.loads(ReceiveData["data"][0]) if "data" in ReceiveData else {}
		else:
			ResumeCandidateInfo = json.loads(ReceiveData["data"]) if "data" in ReceiveData else {}

		if transportType == "file":

			fileContent = ReceiveData["fileContent"] if "fileContent" in ReceiveData else ""
			path = os.path.join(conf.settings.BASE_DIR, 'static', "temporary")
			fileName = str(uuid.uuid1()) + ".docx"

			# 如果目录不存在则创建
			if not os.path.exists(path): os.makedirs(path)

			# 把文件内容保存到本地
			with open(os.path.join(path, fileName), 'wb') as f:
				f.write(base64.b64decode(fileContent))

			filePath = os.path.join(path, fileName)

		elif transportType == "url":

			url = ReceiveData["url"] if "url" in ReceiveData else ""
			if url:
				path = os.path.join(conf.settings.BASE_DIR, 'static', "temporary")
				ResumeTemplateName = os.path.basename(url)
				ResumeTemplateFilePath = os.path.join(path, ResumeTemplateName)
				urllib.request.urlretrieve(url, ResumeTemplateFilePath)

				filePath = ResumeTemplateFilePath
			else:
				ret = {"status": "failed", "status_code": "503", "description": "Pass the wrong Url."}
				return JsonResponse(ret)

		else:
			ret = {"status": "failed", "status_code": "503", "description": "Incorrect transfer, specify the correct 'type' is 'file or url'."}
			return JsonResponse(ret)


		# Check Template
		if not os.path.isfile(filePath):
			ret = {"status": "failed", "status_code": "503", "description": "No valid template is available!"}
			return JsonResponse(ret)

		# # Run main
		WordPath = export.WriteFile(ResumeCandidateInfo, filePath)
		fileContent = open(WordPath, 'rb').read()
		base64Str = base64.b64encode(fileContent).decode("utf-8")
		return HttpResponse(base64Str)
	return JsonResponse(ret)