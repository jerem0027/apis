#!/bin/bash

if [[ "${version}" == "" ]]
then
    echo version is not set please provide version
    exit 1
fi

case "$1" in
    rm)
        docker stop flask-api-${version} && docker rm flask-api-${version}
    ;;
    stop)
        docker stop $(docker ps | grep flask-api | awk '{print $1}')
    ;;
    restart)
        docker restart $(docker ps | grep flask-api | awk '{print $1}')
    ;;
    start|*)
        docker run \
            --network website-network \
            -d -p 5000:5000 \
            --restart unless-stopped \
            --name flask-api-${version} \
            --env-file ./configs/flask.env \
            --ip 172.20.0.10 \
            -v ./certs/:/certs/ \
            jerem0027/server:flask-api-${version}
    ;;
esac