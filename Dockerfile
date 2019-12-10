FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /file_generation_service_repo
WORKDIR /file_generation_service_repo
COPY requirements.txt /file_generation_service_repo/
RUN pip install -r requirements.txt
COPY . /file_generation_service_repo/

FROM ubuntu:latest
RUN \
  apt-get update && \
  apt-get install -y supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
#CMD ["/usr/bin/supervisord"]