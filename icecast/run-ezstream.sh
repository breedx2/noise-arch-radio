#!/bin/bash

MYDIR=$(pwd)

if [ -e /.dockerenv ]; then
	# in container
	source env.sh
	sed -i -e 
	cp /etc/ezstream.xml.template /etc/ezstream.xml
	sed -i -e "s/_ICECAST_HOSTNAME_/${ICECAST_HOSTNAME}/" /etc/icecast/ezstream.xml
	sed -i -e "s/_ICECAST_USER_/${ICECAST_USER}/" /etc/icecast/ezstream.xml
	sed -i -e "s/_ICECAST_PASS_/${ICECAST_PASS}/" /etc/icecast/ezstream.xml
	/usr/bin/ezstream -c /etc/ezstream.xml
else
	# on host
	#docker run --detach \
	docker run -it --rm \
		-v ${MYDIR}/env.sh:/env.sh
		-v ${MYDIR}/ezstream.xml:/etc/ezstream.xml.template \
		-v ${MYDIR}/data:/data \
		--name ezstream \
		ezstream 
fi