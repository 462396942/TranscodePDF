#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import conf
import os, time, datetime, re, shutil, base64, requests, hashlib, json
from contextlib import closing
from ConvertFileFormat import pdfconv
from Storage.controller.upload import upload

NGINX_UOLOAD_ADDRESS = "http://47.95.219.151/upload"

def get_FileMD5(filePath):
    MD5_Object = hashlib.md5()
    maxbuf = 8192
    f = open(filePath,'rb')
    while True:
        buf = f.read(maxbuf)
        if not buf:
            break
        MD5_Object.update(buf)
    f.close()
    md5Code = MD5_Object.hexdigest()
    return  md5Code

def Check_fileName_in_MD5(filePath):
	md5Str = get_FileMD5(filePath)
	if os.path.basename(filePath).split("_")[0] == md5Str:
		fileName = os.path.basename(filePath.split("_")[1])
		os.rename(os.path.join(os.path.dirname(filePath), os.path.basename(filePath)), os.path.join(os.path.dirname(filePath), fileName))
	else:
		fileName = os.path.basename(filePath)
	return fileName


def FileToPDF(sourcefile, tregetfile):
	if os.path.isfile(sourcefile):
		if os.path.splitext(os.path.basename(sourcefile))[1] in [".doc", ".docx", ".txt",".html"]:
			pdfconv.convert_document2pdf(sourcefile, tregetfile)
			return upload(url=NGINX_UOLOAD_ADDRESS, target_file_path=tregetfile)
		else:
			pdfconv._convert_unoconv2pdf(sourcefile, tregetfile)
			return upload(url=NGINX_UOLOAD_ADDRESS, target_file_path=tregetfile)

def CheckExistedPDF(url):
	
	session = requests.get(url)
	if session.status_code == 200:
		
		return False
	else:
		return True

def main(transport_type, fileName=None, fileContent=None, fileMD5=None, url=None):

	if transport_type == "content":

		
		temporaryFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', fileName)

		with open(temporaryFileName, 'wb') as f:
			f.write(base64.b64decode(fileContent))

		fileName = Check_fileName_in_MD5(os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', fileName))
		sourceFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', fileName)
		pdfFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'storage', "".join(fileName.split(".")[:-1]) + ".pdf")
		return FileToPDF(sourceFileName, pdfFileName)
	
	else:
		sourceFileName_inPDF = "".join(os.path.basename(url).split(".")[:-1]) + ".pdf"
		sourceFileTimePath = os.path.basename(os.path.dirname(url))
		check_existedPDF_url = os.path.join("http://47.95.219.151", "firmware", "resume", "pdf", sourceFileTimePath, sourceFileName_inPDF)

		if CheckExistedPDF(check_existedPDF_url):
			temporaryFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', os.path.basename(url))

			session = requests.get(url=url)

			with open(temporaryFileName, 'wb') as f:
				f.write(session.content)

			fileName = Check_fileName_in_MD5(os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', os.path.basename(url)))
			sourceFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', fileName)
			pdfFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'storage', "".join(fileName.split(".")[:-1]) + ".pdf")
			return FileToPDF(sourceFileName, pdfFileName)
		else:
			ret = {
				"account_url": check_existedPDF_url,
			}
			return json.dumps(ret)