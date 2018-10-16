#!/bin/bash
set -e

# https://docs.docker.com/compose/startup-order/
host=$MYSQL_HOST
MYSQL_ROOT_USER=$MYSQL_ROOT_USER
MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD

until MYSQL_ROOT_USER=$MYSQL_ROOT_USER MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -h "$host" -e 'show databases;'; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"


isDatabaseTable=`mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -h "$host" -e "show databases;" | egrep "^$MYSQL_DATABASE$" | wc -l`

if [[ $isDatabaseTable -eq 0 ]]; then 
  echo "NOT Database, Perform create!"
  mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -h "$host" -e "create database $MYSQL_DATABASE character set 'UTF8'"
  mysql -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -h "$host" -e "grant all on $MYSQL_DATABASE.* to $MYSQL_USER@'%' identified by '$MYSQL_PASSWORD'"
fi

python3 manage.py makemigrations

python3 manage.py migrate

sed -i "s/'%s\*\=%s' % (name,\ value)/'%s\="%s"'\ % (name,\ value.encode('utf-8'))/" /usr/local/lib/python3.5/dist-packages/urllib3/fields.py

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
