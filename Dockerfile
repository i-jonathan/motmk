FROM python:3.11-alpine

WORKDIR /app

EXPOSE 8080

RUN pip install --upgrade pip

COPY .env /app/.env

COPY ./requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY . /app