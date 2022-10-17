#!/bin/sh

if [[ $# -eq 0 ]] ; then
    echo 'Please pass in a root directory.'
    exit 0
fi

docker build -t weavegrid-takehome .
docker run -p 5000:5000 -e ROOT_PATH=$1 weavegrid-takehome
