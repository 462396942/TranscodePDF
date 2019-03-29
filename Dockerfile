FROM slzcc/wkhtmltopdf:liboffice
        
RUN	pip3 install --upgrade pip && \
    git clone -b master https://gitee.com/shileizcc_admin/TranscodePDF.git /TranscodePDF

RUN pip install -r /TranscodePDF/package.txt

WORKDIR /TranscodePDF

EXPOSE 8089

COPY docker-entrypoint.sh /docker-entrypoint.sh

CMD /docker-entrypoint.sh