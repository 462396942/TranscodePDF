#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import conf
import os, time, datetime, re, shutil, base64, requests, hashlib, json, chardet
from contextlib import closing
from ConvertFileFormat import pdfconv
from Storage.controller.upload import upload
from ConvertFileFormat.controller import checkFileType


def get_Base64(file_path):
    fileContent = open(file_path, 'rb').read()
    base64Str = base64.b64encode(fileContent).decode("utf-8")
    return base64Str

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
        if os.path.splitext(os.path.basename(sourcefile))[1] in [".html"]:
            pdfconv._convert_wkhtmltopdf(sourcefile, tregetfile, fileCoding)  
            md5Str = get_FileMD5(tregetfile)
            baseStr = get_Base64(tregetfile)

        else:
            pdfconv._convert_unoconv2pdf(sourcefile, tregetfile)
            md5Str = get_FileMD5(tregetfile)
            baseStr = get_Base64(tregetfile)

        # 返回值
        ret = {
            'filename': os.path.basename(tregetfile),
            'md5_str': md5Str,
            'content_type': 'base64',
            'base64_str': baseStr,
            'status': "success",
            'status_code': "200",
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

def _TranscodePDF(url, sourceFile, filePath=None):

    # 检查源文件是 PDF
    if CheckLocalPDF(sourceFile):
        ret = { 
                "status_code": "503", 
                "description": "This is a PDF file!", 
                "status": "failed"
            }
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
        ret = FileToPDF(sourceFile, targetFilePath, fileCoding)
    else:
        ret = FileToPDF(sourceFile, targetFilePath, fileCoding)
    
    if ret:
        ret = json.dumps({ 
                "status_code": "503", 
                "description": "Data transmission error!", 
                "status": "failed"
            })
    return json.dumps(ret)

def main(transport_type, fileName=None, fileContent=None, fileMD5=None, filePath=None, url=None, mp=None):

    if transport_type == "content":
        
        temporaryFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'temporary', fileName)

        with open(temporaryFileName, 'wb') as f:
            f.write(base64.b64decode(fileContent))

        checkFileCoding_inTXT(temporaryFileName)
        fileCoding = getFileCoding(temporaryFileName)

        pdfFileName = os.path.join(conf.settings.BASE_DIR, 'static', 'storage', "".join(fileName.split(".")[:-1]) + ".pdf")
        return json.loads(FileToPDF(temporaryFileName, pdfFileName, fileCoding))
    
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
            try:
                source_file_data = codecs.open(temporaryFileName,'r', encoding='gbk')
            except Exception as e:
                # 获取文件编码
                fileCoding = getFileCoding(sourceFile)
                source_file_data = codecs.open(temporaryFileName,'r', encoding=fileCoding)
            
            eml_obj = email.message_from_file(source_file_data)
            source_file_data.close()
            temporaryFileName = temporaryFileName + ".html"
            temporary_file=open(temporaryFileName,'wb')

            for par in eml_obj.walk():
                current_data=par.get_payload(decode=True)
                if not current_data == None:
                    temporary_file.write(par.get_payload(decode=True))
            temporary_file.close()
        elif FileType in ["html"]:
            temporaryFileName = temporaryFileName + ".html"


        _TranscodePDF(url, md5Str, temporaryFileName, filePath=filePath)
        