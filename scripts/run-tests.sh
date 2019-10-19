#!/bin/sh

dockerfile="FROM python:alpine
WORKDIR /app
COPY . .
ENTRYPOINT [\"python3\", \"./src/main.py\"]"

compose="version: \"3.4\"
services:
  touchstone:
    build: .
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock"

echo "$dockerfile" > Dockerfile
echo "$compose" > docker-compose.yml

docker-compose up --build

rm Dockerfile
rm docker-compose.yml
