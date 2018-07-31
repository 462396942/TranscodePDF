# TranscodePDF

创建数据库:
```
mysql> create database check_md5 character set 'UTF8';
mysql> grant all on check_md5.* to check_md5@'%' identified by 'check_md5';
```

安装启动包：
```
$ pip install -r package.txt
```

Django 创建 Models:
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

Django 创建 User:
```
$ python3 manage.py createsuperuser
```

启动 Django：
```
$ python3 manage.py runserver 8089
```