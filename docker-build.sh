#!/bin/bash

NAME="datamaker"
DOCKERFILE="docker/Dockerfile"

DOCKER=/usr/bin/docker


$DOCKER build -t $NAME .
