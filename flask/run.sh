#!/bin/bash

if [[ "${version}" == "" ]]
then
    echo version is not set please provide version
    exit 1
fi

# Flask API
docker run \
    --network website-network \
    -d -p 5000:5000 \
    --restart unless-stopped \
    --name api-flask \
    --env-file configs/flask.env \
    flask_api:${version}
