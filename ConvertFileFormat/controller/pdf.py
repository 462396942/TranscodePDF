#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import conf
import os, time, datetime, re, shutil, base64, requests
from contextlib import closing
from ConvertFileFormat import pdfconv
import os


def FileToPDF(sourcefile, tregetfile):
	if os.path.isfile(sourcefile):
		if os.path.splitext(os.path.basename(sourcefile))[1] in [".doc", ".docx", ".txt",".html"]:
			pdfconv.convert_document2pdf(sourcefile, tregetfile)
		else:
			pdfconv._convert_unoconv2pdf(sourcefile, tregetfile)

def main(transport_type, fileName=None, fileContent=None, fileMD5=None, url=None):

	if transport_type == "content":
		temporaryFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', fileName)
		pdfFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'storage', "".join(fileName.split(".")[:-1]) + ".pdf")

		with open(temporaryFileName, 'wb') as f:
			f.write(base64.b64decode(fileContent))

		FileToPDF(temporaryFileName, pdfFileName)
	
	else:
		temporaryFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', os.path.basename(url))
		pdfFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'storage', os.path.basename(url).split(".")[:-1] + ".pdf")

		session = requests.get(url=url)
		with open(temporaryFileName, 'wb') as f:
			f.write(session.text)
		FileToPDF(temporaryFileName, pdfFileName)