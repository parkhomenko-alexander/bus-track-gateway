FROM python:3.11.5-slim-bullseye
RUN apt update && apt -y upgrade
WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 2020
ENV PYTHONUNBUFFERED=1

COPY ./ ./