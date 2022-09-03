FROM python3.9-alpine3.12

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
#
RUN apk update \
    && apk add --virtua .build-deps postgresql-dev \
         gcc python3-dev musl-dev librdkafka-dev \
    && apk add librdkafka postgresql-libs libffi-dev make libevent-dev build-base\
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /code/requirements.txt \
    && apk del .build-deps

COPY . /code

ENV PYTHONPATH="/code"
ENV env="test"

EXPOSE 8000

CMD ["python3", "main.py"]
