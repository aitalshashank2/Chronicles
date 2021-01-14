FROM nginx:alpine

LABEL maintainer="Shashank Aital"

RUN rm /etc/nginx/conf.d/default.conf

COPY ./configuration/ /etc/nginx/conf.d/
