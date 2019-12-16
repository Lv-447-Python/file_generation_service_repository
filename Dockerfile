FROM ubuntu:latest
RUN \
  apt-get update && \
  apt-get install -y supervisor python3 python3-pip
RUN mkdir /file_generation_service_repo
WORKDIR /file_generation_service_repo

COPY requirements.txt /file_generation_service_repo/
RUN pip3 install -r requirements.txt
COPY . /file_generation_service_repo/
RUN export PYTHONPATH="${PYTHONPATH}:/file_generation_service_repo"
