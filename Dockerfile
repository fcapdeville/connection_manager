FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y python3.8
#RUN apt-get install -y sudo
RUN apt-get install -y python3-dbus
RUN apt-get install -y net-tools
#RUN apt-get install -y dbus
#RUN apt-get install -y libdbus-glib2.0-cil
#RUN apt-get install -y libdbus-glib2.0-cil-dev
RUN apt-get install -y dbus-x11
#RUN apt-get install -y nano								# adding this to make it easier to the developer