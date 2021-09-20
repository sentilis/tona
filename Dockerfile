FROM node:16-slim AS builder

WORKDIR /usr/app
COPY web /usr/app
RUN npm install
RUN sed -i 's/http:\/\/localhost:5001//g' src/constants/index.js
RUN npm run export

FROM ubuntu:20.04 as runner

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl wkhtmltopdf libmagic-dev\
    python3-pip \
    python3-setuptools

ENV TONA=/tona

RUN mkdir ${TONA}

WORKDIR ${TONA}

COPY MANIFEST.in ${TONA}
COPY README.md ${TONA}
COPY requirements.txt ${TONA}
COPY setup.py ${TONA}
COPY entrypoint.sh ${TONA}

COPY tona/ ${TONA}/tona
COPY --from=builder /usr/app/__sapper__/export/ ${TONA}/tona/templates

RUN pip3 install --upgrade pip
RUN python3 setup.py install

EXPOSE 5001

ENTRYPOINT ["/tona/entrypoint.sh"]

CMD ["tona"]