FROM ubuntu:18.04

RUN apt update

# Use New Zealand mirrors
RUN sed -i 's/archive/nz.archive/' /etc/apt/sources.list

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
  apt-get install -y --no-install-recommends libreoffice-writer \
  python3-dev python3-pip python3-uno python3-setuptools git \
  poppler-utils elinks locales tzdata build-essential \
  libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev && \
  apt upgrade --yes && \
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set timezone to Auckland
RUN locale-gen en_NZ.UTF-8 
RUN dpkg-reconfigure locales
RUN echo "Pacific/Auckland" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
ENV LANG en_NZ.UTF-8
ENV LANGUAGE en_NZ:en

RUN apt update
RUN apt install -y git curl
RUN apt install -y python3-dev python3-pip

RUN pip3 install wheel
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt
