#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import conf
import os, time, datetime, re, shutil, base64, requests, hashlib, json, chardet
from contextlib import closing
from ConvertFileFormat import pdfconv
from Storage.controller.upload import upload
from Repository import models

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

def FileToPDF(sourcefile, tregetfile, fileCoding):
	if os.path.isfile(sourcefile):
		if os.path.splitext(os.path.basename(sourcefile))[1] in [".doc", ".docx", ".txt"]:
			pdfconv._convert_unoconv2pdf(sourcefile, tregetfile)
			return upload(url=conf.settings.NGINX_UOLOAD_ADDRESS, target_file_path=tregetfile)
		else:
			pdfconv._convert_wkhtmltopdf(sourcefile, tregetfile, fileCoding)
			return upload(url=conf.settings.NGINX_UOLOAD_ADDRESS, target_file_path=tregetfile)


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

def main(transport_type, fileName=None, fileContent=None, fileMD5=None, url=None):

	if transport_type == "content":
		
		pass
	
	else:
		temporaryFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', os.path.basename(url))
		session = requests.get(url=url)

		with open(temporaryFileName, 'wb') as f:
			f.write(session.content)

		md5Str = get_FileMD5(temporaryFileName)
		obj = models.MD5.objects.filter(file_source_md5=md5Str)

		# 校验是否已经被解析
		if obj.exists():
			PDFAddress = obj.last().file_pdf_address
			print(PDFAddress,type(PDFAddress))
			ret = {
				"account_url": PDFAddress,
			}
			return ret

		else:
			# 源文件目录
			fileName=os.path.basename(url)
			sourceFilePath = os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', fileName)

			# 目标文件目录
			sourceFileName_inPDF = "".join(os.path.basename(url).split(".")[:-1]) + ".pdf"
			targetFilePath = os.path.join(conf.settings.BASE_DIR, 'static', 'storage', sourceFileName_inPDF)

			# 目标文件最终存储 Url
			sourceFileTimePath = "/".join(url.split("/")[3:-1])
			storagePDFAddress = os.path.join(conf.settings.NGINX_MIRROR_ADDRESS, sourceFileTimePath, sourceFileName_inPDF)

			# 检测文件是否 TXT，如果是则重写文件编码
			checkFileCoding_inTXT(temporaryFileName)
			
			# 获取文件编码
			fileCoding = getFileCoding(temporaryFileName)
			
			# 生成 PDF
			ret =  json.loads(FileToPDF(temporaryFileName, targetFilePath, fileCoding))

			# 写入数据库
			data = {
				"file_source_md5": md5Str,
				"file_source_address": url,
				"file_pdf_md5": ret["md5"],
				"file_pdf_address": ret["account_url"],
			}
			models.MD5.objects.create(**data)

			return ret