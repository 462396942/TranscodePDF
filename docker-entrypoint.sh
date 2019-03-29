#!/bin/bash
set -e

exec uwsgi --socket 0.0.0.0:18089 \
      --chdir /TranscodePDF/ \
      --env DJANGO_SETTINGS_MODULE=TranscodePDF.settings \
      --module "django.core.handlers.wsgi:WSGIHandler()" \
      --processes 4 \
      --threads 2 \
      --workers 5 \
      --http 0.0.0.0:8089 \
      --uid root --gid root \
      --master --vacuum \
      --thunder-lock \
      --enable-threads \
      --harakiri 30 \
      --post-buffering 4096 \
      --file "/TranscodePDF/TranscodePDF/wsgi.py"
