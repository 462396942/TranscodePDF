#!/bin/bash
set -e

# https://docs.docker.com/compose/startup-order/
host=$MYSQL_HOST

until MYSQL_USER=$MYSQL_USER MYSQL_PASSWORD=$MYSQL_PASSWORD mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -h "$host" -e 'use resume;'; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"

python3 manage.py migrate

sed -i "s/'%s\*\=%s' % (name,\ value)/'%s\="%s"'\ % (name,\ value.encode('utf-8'))/" /usr/local/lib/python3.5/site-packages/urllib3/fields.py

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
