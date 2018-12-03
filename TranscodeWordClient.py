#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests, json, base64, urllib

resume = {
            1: "项目经验$|_@2017-07 ~ 至今\n微信核保系统 \n 所属公司: 中科软科技股份有限公司 \n   项目简介   系统前端采用jQuery-EasyUI,后端采用ssm和MySQL,部署在Linux服务器上,使用sso单点登录加redis来解决系统应用群的问题。为提升承保效率由传统核保模式转换成微信核保模式,在微信端实现线上核保函件,系统下发函件,通过微信端企业号推送下发电子函件信息给代理人,代理人转发函件下发链接给客户,完成核保函件线上下发、回销,项目使用Quartz实现与核心接口的定时跑批任务。项目兼顾线上线下功能,实现客户和营销员的全自动化 \n 责任描述: 完成基础代码模块的开发;配合测试人员完成bug修改,编写项目文档2016-08 ~ 2017-05\n团险核心系统 \n 所属公司: 青岛松立软件科技有限公司 \n   项目简介   基于ssm的多层框架。展现层使用SpringMVC来实现MVC模式。保全业务在录入有误或有保全自核提示时,在人工核保时录入保全问题件,保全问题件录入完毕后流转至保全问题件修改,这时保全问题件录入回退给操作员时,直接进行问题件修改并回复,保全问题件修改确定后流转至人工核保,人工核保没问题后保全确认;保全问题件录入回退的是客户和业务员时,需要先打印保全变更通知书,至客户和业务员确认签字后,进行问题件回销(手工回销或扫描回销)后进行问题件修改并回复,问题件修改确认后,至自动核保。 \n 责任描述: 配合完成基础模块代码的开发2015-10 ~ 2016-07\n企业运营管理系统 \n 所属公司: 青岛松立软件科技有限公司 \n   项目简介   T服务管理系统,帮组企业对IT系统的规划、实施和运营进行管理,系统前端采用jQuery-EasyUI,后端采用ssm和MySQL,部署在Linux服务器上。系统主要包括:事件管理、投诉管理、配置变更发布管理、问题管理、巡检管理、替班管理、合同管理、知识共享、决策分析等功能。 \n 责任描述: 负责项目的需求分析,部分模块设计和编码工作",
            2: "工作经验$|_@2017-07 ~ 至今 中科软科技股份有限公司 互联网软件开发工程师 | 行业解决事业部 [ 10个月] 互联网/电子商务 | 5000-10000人 | 国企 工作描述: 负责项目的需求分析工作,按照需求完成基础代码模块的开发;配合测试人员完成bug的修改;编写项目文档。2015-06 ~ 2017-05 青岛松立软件科技有限公司 互联网软件开发工程师 | 金融事业部 [ 1年11个月] 互联网/电子商务 | 500-1000人 | 民营公司 工作描述: 负责项目的需求分析工作,按照需求完成基础代码模块的开发;配合测试人员完成bug的修改;编写项目文档。",
            3: "教育经验$|_@2012-09 ~ 2015-09 山东理工职业学院 大专 | 计算机信息管理",
            4: "个人介绍$|_@框架:ssm(SpringMVC、Spring、MyBatis) 数据库:MySQL、Redis 前端:JavaScript、JSP、jQuery WEB容器:Tomcat 操作系统:Linux 开发工具:SVN、Maven、Eclipse、MyEclipse,git",
            "BaseInfo": {
                3: "出生日期|1994-05-23",
                2: "性别|男",
                4: "最高学历|大专",
                1: "姓名|胡某某",
            }
        }
## ****************************** url methods ************************************
url = "http://127.0.0.1:8089/api/v1/file/word"
data = {"data": json.dumps(resume), "type": "url", "url": "http://35.229.131.32/firmware/resume/templates/Hydsoft%20Candidate%20CV-Position-Name-CN.docx"}
session = requests.post(url, data=data)
	
## ****************************** base64 methods ************************************
#path="/Users/shilei/Desktop/Hydsoft Candidate CV-Position-Name-CN.docx"
#url = "http://127.0.0.1:8089/api/v1/file/word"
#
#fileContent = open(path, 'rb').read()
#base64Str = base64.b64encode(fileContent).decode("utf-8")
#
#data = {"type": "file", "fileContent": base64Str, "data": json.dumps(resume)}
#session = requests.post(url, data=data)

# ****************************** Save ************************************
with open("/Users/shilei/Desktop/demo.docx", 'wb') as f:
	f.write(base64.b64decode(session.text))