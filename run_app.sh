#!/bin/sh

docker build -t weavegrid-takehome .
docker run -p 5000:5000 -e ROOT_PATH=$1 weavegrid-takehome
