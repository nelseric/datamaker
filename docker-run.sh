#!/bin/bash

NAME="datamaker"
DOCKERFILE="docker/Dockerfile"

DOCKER=/usr/bin/docker

DATA_PATH="`pwd`/data"
DATA_DEST="/root/datamaker/data"


$DOCKER run -p 54321:54321 -v $DATA_PATH:$DATA_DEST --name $NAME -t $NAME
