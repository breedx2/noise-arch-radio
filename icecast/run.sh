#!/bin/bash

EXTPORT=9123
MYDIR=$(pwd)

if [ ! -e ${MYDIR}/access.log ] ; then
	touch ${MYDIR}/access.log
fi
if [ ! -e ${MYDIR}/error.log ] ; then
	touch ${MYDIR}/error.log
fi

docker run -it --rm \
	-p ${EXTPORT}:8000 \
	-v ${MYDIR}/icecast.xml:/etc/icecast/icecast.xml \
	--name icecast2 \
	icecast2 
