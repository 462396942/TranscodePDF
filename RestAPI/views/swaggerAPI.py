#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf

import os, time, requests, json, datetime, re, shutil

def SwaggerAPI(request):

	ret = {
		"swaggerVersion": "1.0",
		"apis": [
			{
				"path": "/api/v1",
				"description": "API at /api/v1 ."
			},
			{
				"path": "/api/v1/file",
				"description": "An API for file processing."
			},
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