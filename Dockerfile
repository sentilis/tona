FROM python:3.8-alpine

ENV TONA=/tona

RUN mkdir ${TONA}
WORKDIR ${TONA}

COPY ./ ${TONA}

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

EXPOSE 5001

CMD ["cmd/main.py", "webapp"]