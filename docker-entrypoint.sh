#!/bin/bash
set -x 

sed -i "s/'%s\*\=%s' % (name,\ value)/'%s\="%s"'\ % (name,\ value.encode('utf-8'))/" /usr/local/lib/python3.7/site-packages/urllib3/fields.py

exec uwsgi --socket 0.0.0.0:8877 \
      --chdir /UploadInterface/ \
      --env DJANGO_SETTINGS_MODULE=UploadInterface.settings \
      --module "django.core.handlers.wsgi:WSGIHandler()" \
      --processes 4 \
      --threads 2 \
      --workers 5 \
      --http 0.0.0.0:8878 \
      --uid root --gid root \
      --master --vacuum \
      --thunder-lock \
      --enable-threads \
      --harakiri 30 \
      --post-buffering 4096 \
      --file "/UploadInterface/UploadInterface/wsgi.py"
