#!/bin/bash

if [[ "${version}" == "" ]]
then
    echo version is not set please provide version
    exit 1
fi

docker push jerem0027/server:flask-api-${version}