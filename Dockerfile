FROM python:3

MAINTAINER Sammor

ADD . /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

EXPOSE 8000

WORKDIR lolinfo

CMD exec gunicorn lolinfo.wsgi --bind 0.0.0.0:8000
