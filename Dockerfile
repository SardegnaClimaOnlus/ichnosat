# ==================================================================================== #
#  __     ______     __  __     __   __     ______     ______     ______     ______
# /\ \   /\  ___\   /\ \_\ \   /\ "-.\ \   /\  __ \   /\  ___\   /\  __ \   /\__  _\
# \ \ \  \ \ \____  \ \  __ \  \ \ \-.  \  \ \ \/\ \  \ \___  \  \ \  __ \  \/_/\ \/
#  \ \_\  \ \_____\  \ \_\ \_\  \ \_\\"\_\  \ \_____\  \/\_____\  \ \_\ \_\    \ \_\
#   \/_/   \/_____/   \/_/\/_/   \/_/ \/_/   \/_____/   \/_____/   \/_/\/_/     \/_/
#
# ==================================================================================== #
#
# Copyright (c) 2017 Sardegna Clima - Raffaele Bua (buele)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ==================================================================================== #

FROM debian

# Create app directory
RUN mkdir -p /usr/ichnosat

# install depenpendencies
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y build-essential
RUN apt-get install -y unzip
RUN apt-get install -y cmake

#install openjpeg
WORKDIR /usr
RUN mkdir -p /usr/openjpeg
WORKDIR /usr/openjpeg
COPY vendors/openjpeg-2.1.1.zip /usr/openjpeg
RUN unzip openjpeg-2.1.1.zip
WORKDIR /usr/openjpeg/openjpeg-2.1.1
RUN mkdir build
WORKDIR /usr/openjpeg/openjpeg-2.1.1/build
RUN cmake ..
RUN make
RUN make install
RUN make clean
RUN ln -s /usr/local/lib/libopenjp2.so.7 /usr/lib/
WORKDIR /usr
RUN rm -rf /usr/openjpeg

#install gdal
WORKDIR /usr
RUN mkdir -p /usr/gdal
WORKDIR /usr/gdal
COPY vendors/gdal212.zip /usr/gdal
RUN unzip gdal212.zip
WORKDIR /usr/gdal/gdal-2.1.2
RUN ./configure --with-openjpeg=/usr/local
RUN make
RUN make install
WORKDIR /usr
RUN rm -rf gdal

#install python and pip
RUN apt-get install -qy python3.4
WORKDIR /usr/pip
RUN mkdir -p /usr/pip
COPY vendors/get-pip.py /usr/pip
RUN ls
RUN python3.4 get-pip.py
WORKDIR /usr


# install pika
RUN pip install pika

#install flask
RUN pip install Flask
RUN pip install -U flask-cors

#install wget
RUN apt-get install -y wget

# install sqlalchemy
RUN pip install sqlalchemy


RUN mkdir -p /usr/ichnosat/server

RUN export PYTHONPATH=${PYTHONPATH}:/usr/ichnosat
WORKDIR /usr/ichnosat/
RUN apt-get update
RUN apt-get install -qy python2.7
WORKDIR /usr/pip
RUN python2.7 get-pip.py
RUN python2.7 -m pip install supervisor

## install postgres
RUN apt-get update
RUN apt-get install -y  libpq-dev postgresql-client postgresql-client-common
RUN apt-get install -y  python3-psycopg2

##install crontab
RUN apt-get install -y cron
RUN apt-get install -y python3-crontab

## install valgrind
RUN apt-get install -y valgrind

RUN pip3 install Sphinx
RUN apt-get install -y vim


WORKDIR /usr/ichnosat/




