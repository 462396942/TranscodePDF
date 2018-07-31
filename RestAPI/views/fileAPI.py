#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf
from ConvertFileFormat.controller.pdf import main
import os, time, requests, json, datetime, re, shutil
from django.utils.safestring import mark_safe

def GetFileAPI(request):
	ret = {
		"apis":[
			{
				"path": "/api/v1/file/pdf",
				"description": "Process files into PDF format."
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
					"mandatory_parsing": "False",
				}
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
			fileMD5 = ReceiveData["fileMD5"] if "fileMD5" in ReceiveData else _emptyData.append("fileMD5")
		elif transportType == "url":
			_url = ReceiveData["url"] if "url" in ReceiveData else _emptyData.append("url")
			mp = ReceiveData["mandatory_parsing"] if "mandatory_parsing" in ReceiveData else "False"
			mp = True if mp == "True" else False
		else:
			ret = {"status": "failed", "status_code": "503", "description": "Incorrect transfer, specify the correct 'type' is 'content or url'."}
			return JsonResponse(ret)

		# Determine whether there is free data
		if _emptyData:
			ret = {"status": "failed", "status_code": "503", "description": "Lack of necessary data '{}'.".format(", ".join(_emptyData))}
			return JsonResponse(ret)

		# Run main
		if transportType == "url":
			ret = main(
				transport_type=transportType, 
				url=_url,
				mp=mp
			)
	return JsonResponse(ret)