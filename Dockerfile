FROM python:3.9.6-slim-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN python -m pip install -r requirements.txt

COPY . .
