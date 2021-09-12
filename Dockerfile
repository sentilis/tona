FROM debian:buster-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    python3-pip \
    python3-setuptools \
    && curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb \
    && echo 'ea8277df4297afc507c61122f3c349af142f31e5 wkhtmltox.deb' | sha1sum -c - \
    && apt-get install -y --no-install-recommends ./wkhtmltox.deb \
    && rm -rf /var/lib/apt/lists/* wkhtmltox.deb

ENV TONA=/tona

RUN mkdir ${TONA}
RUN mkdir -p ${TONA}/storage

WORKDIR ${TONA}

COPY ./ ${TONA}

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 setup.py install

EXPOSE 5001

ENTRYPOINT ["/tona/entrypoint.sh"]

CMD ["tona"]