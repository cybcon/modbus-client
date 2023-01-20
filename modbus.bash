#!/bin/bash

OPTIONS=${@}

## Project settings
#if [ -z "`echo ${OPTIONS} | grep '\-t '`" ]; then
#  OPTIONS="-t 4 ${OPTIONS}"
#fi
#if [ -z "`echo ${OPTIONS} | grep '\-p '`" ]; then
#  OPTIONS="-p 1503 ${OPTIONS}"
#fi
#if [ -z "`echo ${OPTIONS} | grep '\-s '`" ]; then
#  OPTIONS="-s 192.168.58.70 ${OPTIONS}"
#fi

docker run --rm oitc/modbus-client:latest ${OPTIONS}
