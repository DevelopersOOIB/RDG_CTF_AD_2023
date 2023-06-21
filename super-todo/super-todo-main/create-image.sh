#!/usr/bin/env bash

IMAGE_NAME=super-todo

mvn -U clean install

docker build -t $IMAGE_NAME .

# get image info
docker image ls | grep $IMAGE_NAME