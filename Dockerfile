FROM python:3.11-slim-buster

RUN apt-get update && apt-get upgrade -y && apt-get install -y gcc g++  libpq-dev
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app .

CMD [ "gunicorn", "view:app" ,"-b 0.0.0.0:8080"]