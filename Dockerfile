FROM python:3.7.2-alpine3.9

RUN apk add  \
    openblas-dev \
    gfortran \
    alpine-sdk

COPY ./requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt

# Snake module (in PYTHONPATH)
ARG SNAKE_MOD=twistedsister.snake:application

COPY . /home/app

# TODO: support multiple snakes?
WORKDIR /home/app
RUN echo ${SNAKE_MOD} > snake_mod.txt

EXPOSE 80
ENTRYPOINT gunicorn $(cat snake_mod.txt) -b 0.0.0.0:80
