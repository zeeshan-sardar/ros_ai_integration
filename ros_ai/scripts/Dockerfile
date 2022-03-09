# syntax=docker/dockerfile:1
FROM ubuntu:18.04

COPY . /app
RUN apt update && apt install -y python3 python3-numpy python3-opencv 
RUN apt install -y python3-pip
RUN pip3 install pybase64 jsonpickle Flask

CMD python3 /app/server.py