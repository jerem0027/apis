#!/bin/bash

export version=$(cat app/server/envconfig_prod.py | grep "API_VERSION" | grep -Po "API_VERSION = .\K([0-9]+\.[0-9]+(\.[0-9]+)?)")

echo ${version}
