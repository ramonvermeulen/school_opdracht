FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install apache2
RUN apt-get -y install python3-pip

RUN a2enmod cgi
RUN service apache2 restart

ADD . /usr/lib/cgi-bin
RUN chmod -R 705 /usr/lib/cgi-bin
RUN mkdir /data
RUN chmod -R 775 /data

RUN ["pip3", "install", "-r", "/usr/lib/cgi-bin/requirements.txt"]

CMD /usr/sbin/apache2ctl -D FOREGROUND