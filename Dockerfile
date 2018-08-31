FROM slzcc/wkhtmltopdf:liboffice

RUN apt update && \
	apt install -y mysql-client-core-5.7 && \
	apt-get autoremove --purge --yes && \
    rm --force --recursive \
        /tmp/* \
        /var/lib/apt/lists/*
        
RUN	pip3 install --upgrade pip && \
    git clone -b database_model https://gitee.com/shileizcc_admin/TranscodePDF.git /TranscodePDF

RUN pip install -r /TranscodePDF/package.txt

WORKDIR /TranscodePDF

ENV MYSQL_DATABASE=check_md5 \
    MYSQL_USER=check_md5 \
    MYSQL_PASSWORD=check_md5 \
    MYSQL_HOST="172.17.0.2" \
    MYSQL_PORT=3306 \
    NGINX_MIRROR_ADDRESS="http://127.0.0.1/"

EXPOSE 8089

COPY docker-entrypoint.sh /docker-entrypoint.sh

CMD /docker-entrypoint.sh