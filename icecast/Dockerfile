FROM debian:latest

RUN apt update && apt install -y icecast2

RUN touch /var/log/icecast2/access.log /var/log/icecast2/error.log
RUN chown -R icecast2:icecast /var/log/icecast2

CMD /usr/bin/icecast2 -c /etc/icecast/icecast.xml
