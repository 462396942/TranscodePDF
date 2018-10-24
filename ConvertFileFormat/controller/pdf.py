#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import conf
import os, time, datetime, re, shutil, base64, requests, hashlib, json, chardet
from contextlib import closing
from ConvertFileFormat import pdfconv
from Storage.controller.upload import upload
from Repository import models
from ConvertFileFormat.controller import checkFileType


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

def FileToPDF(sourcefile, tregetfile, fileCoding, uploadPath):
	if os.path.isfile(sourcefile):
		if os.path.splitext(os.path.basename(sourcefile))[1] in [".doc", ".docx", ".txt"]:
			pdfconv._convert_unoconv2pdf(sourcefile, tregetfile)
			ret = upload(url=conf.settings.NGINX_UPLOAD_ADDRESS, target_file_path=tregetfile, path=uploadPath)
			print(ret)
			return ret
		elif os.path.splitext(os.path.basename(sourcefile))[1] in [".html"]:
			pdfconv._convert_wkhtmltopdf(sourcefile, tregetfile, fileCoding)
			ret = upload(url=conf.settings.NGINX_UPLOAD_ADDRESS, target_file_path=tregetfile, path=uploadPath)
			print(ret)
			return ret
		else:
			ret = { 
				"status_code": "503", 
				"description": "Support for parsing file suffixes '.doc, .docx, .txt, .html', Please modify the correct file suffix after re-upload!", 
				"status": "failed"
			}
			return json.dumps(ret)

def getFileCoding(filePath):
	with open(filePath, 'rb') as f:
		obj = f.read()
	return chardet.detect(obj)["encoding"]

def checkFileCoding_inTXT(filePath):
	if os.path.splitext(os.path.basename(filePath))[1] in [".txt"]:
		try:
			with open(filePath, 'r', encoding='gbk') as f:
				SourceContent = f.read()
			os.remove(filePath)
			with open(filePath, 'w', encoding='utf-8') as f:
				f.write(SourceContent)
		except UnicodeDecodeError:
			pass
	else:
		return

def CheckExistedPDF(url):
	
	session = requests.get(url)
	if session.status_code == 200:
		
		return True
	else:
		return False

def CheckLocalPDF(Path):

	FileType = checkFileType.filetype(Path)
	if FileType in ["pdf"]:
		return True
	else:
		return False

def _TranscodePDF(url, md5Str, sourceFile, filePath=None):

	# 检查源文件是 PDF
	if CheckLocalPDF(sourceFile):
		ret = json.loads("This is a PDF file!")
		return ret

	# 源文件目录
	fileName=os.path.basename(url)
	sourceFilePath = os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', fileName)

	# 目标文件目录
	sourceFileName_inPDF = "".join(fileName.split(".")[:-1]) + ".pdf"
	targetFilePath = os.path.join(conf.settings.BASE_DIR, 'static', 'storage', sourceFileName_inPDF)

	# Get Url Subdirectories
	sourceFileSubPath = "/".join(url.split("/")[3:-1])

	# 检测文件是否 TXT，如果是则重写文件编码
	checkFileCoding_inTXT(sourceFile)
	
	# 获取文件编码
	fileCoding = getFileCoding(sourceFile)
	
	# 生成 PDF
	if filePath:
		response = FileToPDF(sourceFile, targetFilePath, fileCoding, os.path.join(filePath))
		print(response,sourceFile, targetFilePath, fileCoding, os.path.join(sourceFileSubPath))
		ret = json.loads(response)
	else:
		response = FileToPDF(sourceFile, targetFilePath, fileCoding, os.path.join(sourceFileSubPath))
		print(response,sourceFile, targetFilePath, fileCoding, os.path.join(sourceFileSubPath))
		ret = json.loads(response)

	if "status_code" in ret.keys():
		if ret["status_code"] == "503":
			return ret
			
	# 写入数据库
	data = {
		"file_source_md5": md5Str,
		"file_source_address": url,
		"file_pdf_md5": ret["md5"],
		"file_pdf_address": ret["account_url"],
	}
	try:
		models.MD5.objects.create(**data)
	except:
		models.MD5.objects.filter(file_source_md5=md5Str).delete()
		_TranscodePDF(url, md5Str, sourceFile)
	return ret

def main(transport_type, fileName=None, fileContent=None, fileMD5=None, filePath=None, url=None, mp=None):

	if transport_type == "content":
		
		temporaryFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', fileName)

		with open(temporaryFileName, 'wb') as f:
			f.write(base64.b64decode(fileContent))

		checkFileCoding_inTXT(temporaryFileName)
		fileCoding = getFileCoding(temporaryFileName)

		pdfFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'storage', "".join(fileName.split(".")[:-1]) + ".pdf")
		return json.loads(FileToPDF(temporaryFileName, pdfFileName, fileCoding, os.path.join(filePath)))
	
	else:

		temporaryFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', os.path.basename(url))
		session = requests.get(url=url)

		with open(temporaryFileName, 'wb') as f:
			f.write(session.content)

		# 判断文件类型, 如果是 eml 则解析原内容
		FileType = checkFileType.filetype(temporaryFileName)
		if FileType in ["eml"]:
			import codecs
			import email

			source_file_data = codecs.open(temporaryFileName,'r', encoding='gbk')
			eml_obj = email.message_from_file(source_file_data)
			source_file_data.close()

			temporary_file=open(temporaryFileName,'wb')

			for par in eml_obj.walk():
				current_data=par.get_payload(decode=True)
				if not current_data == None:
					temporary_file.write(par.get_payload(decode=True))
			temporary_file.close()

		md5Str = get_FileMD5(temporaryFileName)

		if not mp:
			obj = models.MD5.objects.filter(file_source_md5=md5Str)

			# 校验是否已经被解析
			if obj.exists():
				PDFAddressUrl = obj.last().file_pdf_address
				if CheckExistedPDF(PDFAddressUrl):
					ret = {
						"account_url": PDFAddressUrl,
					}
					return ret
				else:
					return _TranscodePDF(url, md5Str, temporaryFileName, filePath=filePath)
				
			else:
				return _TranscodePDF(url, md5Str, temporaryFileName, filePath=filePath)
		else:
			return _TranscodePDF(url, md5Str, temporaryFileName, filePath=filePath)
		