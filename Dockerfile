FROM python:3.10

WORKDIR /app

EXPOSE 5000

ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .