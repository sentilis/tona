FROM python:3.8-alpine

RUN apk update && apk upgrade && apk add bash

ENV TONA=/tona

RUN mkdir ${TONA}
RUN mkdir -p ${TONA}/storage

WORKDIR ${TONA}

COPY ./ ${TONA}

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python setup.py install

EXPOSE 5001

ENTRYPOINT ["/tona/entrypoint.sh"]

CMD ["tona"]