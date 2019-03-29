FROM slzcc/wkhtmltopdf:liboffice

RUN apt update && \
	apt install -y mysql-client-core-5.7 && \
	apt-get autoremove --purge --yes && \
    rm --force --recursive \
        /tmp/* \
        /var/lib/apt/lists/*
        
RUN	pip3 install --upgrade pip && \
    git clone -b master https://gitee.com/shileizcc_admin/TranscodePDF.git /TranscodePDF

RUN pip install -r /TranscodePDF/package.txt

WORKDIR /TranscodePDF

EXPOSE 8089

COPY docker-entrypoint.sh /docker-entrypoint.sh

CMD /docker-entrypoint.sh