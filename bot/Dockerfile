# pull official base image
FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/bot

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt /usr/src/bot/requirements.txt
RUN pip3 install -r requirements.txt


# copy project
COPY . /usr/src/bot/