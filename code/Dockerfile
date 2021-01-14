FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /Chronicles
WORKDIR /Chronicles

COPY . .

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc mariadb-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev

RUN pip install -r requirements.txt

EXPOSE 8000
EXPOSE 3306

CMD ["python", "manage.py", "runserver"]