FROM python:3.8
WORKDIR /bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /bot/requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install netcat -y

COPY . /bot