#!/bin/bash

MYDIR=$(pwd)

#docker run --detach \
docker run -it --rm \
	-v ${MYDIR}/ezstream.xml:/etc/ezstream.xml \
	-v ${MYDIR}/data:/data \
	--name ezstream \
	ezstream 
