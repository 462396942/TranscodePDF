FROM slzcc/wkhtmltopdf:liboffice

RUN	pip3 install --upgrade pip && \
    mkdir /TranscodePDF

WORKDIR /TranscodePDF
COPY . .

RUN pip install -r package.txt

EXPOSE 8089

COPY docker-entrypoint.sh /docker-entrypoint.sh

CMD /docker-entrypoint.sh
