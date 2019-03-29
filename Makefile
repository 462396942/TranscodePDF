SHELL := /bin/bash
VERSION := "v0.4.0"
build:
	@docker build -t slzcc/transcode:$(VERSION) . --no-cache
push:
	@docker push slzcc/transcode:$(VERSION)
