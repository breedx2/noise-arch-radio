#!/bin/bash

EXTPORT=9123
MYDIR=$(pwd)

if [ -e /.dockerenv ]; then
	# In container
	source /env.sh
	cp /etc/icecast/icecast.xml.template /etc/icecast/icecast.xml
	sed -i -e "s/_ICECAST_HOSTNAME_/${ICECAST_HOSTNAME}/" /etc/icecast/icecast.xml
	sed -i -e "s/_ICECAST_ADMIN_USER_/${ICECAST_ADMIN_USER}/" /etc/icecast/icecast.xml
	sed -i -e "s/_ICECAST_ADMIN_PASS_/${ICECAST_ADMIN_PASS}/" /etc/icecast/icecast.xml
	sed -i -e "s/_ICECAST_CLIENT_USER_/${ICECAST_CLIENT_USER}/" /etc/icecast/icecast.xml
	sed -i -e "s/_ICECAST_CLIENT_PASS_/${ICECAST_CLIENT_PASS}/" /etc/icecast/icecast.xml
	/usr/bin/icecast2 -c /etc/icecast/icecast.xml
else
	# In host
	#docker run -it --rm \
	docker run --detach \
		-p ${EXTPORT}:8000 \
		-v ${MYDIR}/env.sh:/env.sh \
		-v ${MYDIR}/icecast.xml:/etc/icecast/icecast.xml.template \
		--name icecast2 \
		icecast2 
fi

