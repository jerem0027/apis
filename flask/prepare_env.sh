#!/bin/bash


if [ -d ./virtualenv ]
then
    source ./virtualenv/bin/activate
else
    virtualenv -p python3 virtualenv
    source virtualenv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

export LOCAL_PATH=~/realtemp

mkdir $LOCAL_PATH/files

cp -r app/static $LOCAL_PATH