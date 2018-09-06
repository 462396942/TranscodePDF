# TranscodePDF

详细的使用请先通过 Docker Compose 启动服务：
```
$ docker-compose up -d
```

### Transcode in PDF
如果需要解析成 PDF，请参照 TranscodePDFClient.py 文件代码执行所需操作。
主要说明的是目前支持传递 html/txt/docx/doc 文件格式转码 PDF。
(由于自身服务的需要，此方法配合了 MySQl 作为存储，如果检测文件 MD5 值已经记录在内，则不进行解析，并返回解析后保存的地址，此服务后端存储需要配合[Nginx Upload](https://gitee.com/shileizcc_admin/Django-Upload-Files/tree/nginx_upload/), 可传递 `mandatory_parsing` 参数强制解析.) 
PDF 支持两种方式，url 与 content，具体请参照示例。

### Transcode in Word
如果需要解析成 Word，请参照 TranscodeWordClient.py 文件代码执行所需操作。
主要说明，此服务属于自身业务所需而构建的，主要应用于原始数据导出 Word，所以需要两部分，一部分为 Data，一部分 Word Template，最后通过 Template 导出一份拼接好的文件内容。（Template 不支持空数据）
Template 支持两种方式，url 与 content，具体请参照示例。

[Wiki Docs Url](https://wiki.shileizcc.com/confluence/display/CASE/Django+TranscodePDF)
| Wiki 暂未更新