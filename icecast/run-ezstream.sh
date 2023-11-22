#!/bin/bash

MYDIR=$(pwd)

if [ -e /.dockerenv ]; then
	# in container
	source env.sh
	cp /etc/ezstream.xml.template /etc/ezstream.xml
	sed -i -e "s/_ICECAST_HOSTNAME_/${ICECAST_HOSTNAME}/" /etc/ezstream.xml
	sed -i -e "s/_ICECAST_CLIENT_USER_/${ICECAST_CLIENT_USER}/" /etc/ezstream.xml
	sed -i -e "s/_ICECAST_CLIENT_PASS_/${ICECAST_CLIENT_PASS}/" /etc/ezstream.xml
	chmod 600 /etc/ezstream.xml
	/usr/bin/ezstream -c /etc/ezstream.xml
else
	# on host
	#docker run --detach \
	docker run -it --rm \
		-v ${MYDIR}/env.sh:/env.sh \
		-v ${MYDIR}/ezstream.xml:/etc/ezstream.xml.template \
		-v ${MYDIR}/../data:/data \
		--name ezstream \
		ezstream 
fi