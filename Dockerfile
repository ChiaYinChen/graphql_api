FROM python:3.8.0-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN mkdir /graphql_api
WORKDIR /graphql_api
COPY . /graphql_api
RUN pip install -r requirements.txt
