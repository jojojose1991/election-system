FROM python:3.7

COPY requirements.txt /
RUN set -ex \
    && pip install -r requirements.txt

