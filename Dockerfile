FROM python:3.7.3-slim

WORKDIR /app

COPY .. .

RUN pip install --upgrade pip

RUN pip install -r ./requirements.txt

ARG SERVER_PORT

ENV SERVER_PORT=$SERVER_PORT

ENTRYPOINT ["bash","./gunicorn.sh"]