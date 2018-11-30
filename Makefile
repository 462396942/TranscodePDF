SHELL := /bin/bash
VERSION := "0.3.15"
build:
	@docker build -t slzcc/transcode:$(VERSION) . --no-cache
push:
	@docker push slzcc/transcode:$(VERSION)
set_data:
	@docker exec -t transcode-mysql mysql -uroot -pexample.org -e "create database check_md5 character set 'UTF8';"
	@docker exec -t transcode-mysql mysql -uroot -pexample.org -e "grant all on check_md5.* to check_md5@'%' identified by 'check_md5';"
	@docker exec -t transcode python3 manage.py migrate
