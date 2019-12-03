FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /file_generation_service_repo
WORKDIR /file_generation_service_repo
COPY requirements.txt /file_generation_service_repo/
RUN pip install -r requirements.txt
COPY . /file_generation_service_repo/