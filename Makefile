SHELL := /bin/bash
VERSION := "1"
build:
	@docker build -t slzcc/django:transcode-pdf-uwsgi-v$(VERSION) . --no-cache
push:
	@docker push slzcc/django:transcode-pdf-uwsgi-v$(VERSION)