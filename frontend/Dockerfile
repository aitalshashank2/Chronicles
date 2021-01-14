FROM node:14.4.0-alpine3.10

LABEL maintainer="Shashank Aital"

USER root

RUN mkdir /frontend

WORKDIR /frontend

COPY ./Chronicles-Frontend/ .

RUN npm install

RUN npm run build
