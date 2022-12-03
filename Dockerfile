FROM python:3
MAINTAINER Dany

ENV PYTHONUNBUFFERED = 1
WORKDIR usr/src/app
COPY requirements.txt ./

RUN pip install -r requirements.txt

RUN adduser -D user
USER user