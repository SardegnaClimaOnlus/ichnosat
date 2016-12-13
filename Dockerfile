FROM debian

# Create app directory
#RUN mkdir -p /usr/ichnosat/downloader
#RUN mkdir -p /usr/ichnosat/post-processor
#RUN mkdir -p /usr/ichnosat/pre-processor
#RUN mkdir -p /usr/ichnosat/scientific-processor
RUN mkdir -p /usr/ichnosat



# install depenpendencies
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y build-essential
RUN apt-get install -y unzip
RUN apt-get install -y cmake


# Bundle app source
#COPY downloader/ /usr/ichnosat/downloader/
#COPY post-processor/ /usr/ichnosat/post-processor/
#COPY pre-processor/ /usr/ichnosat/pre-processor/
#COPY scientific-processor/ /usr/ichnosat/scientific-processor

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
RUN rm -rf pip

# install pika
RUN pip install pika

#install flask
RUN pip install Flask

#install wget
RUN apt-get install -y wget


# install rabbitmq
RUN echo 'deb http://www.rabbitmq.com/debian/ testing main' | tee /etc/apt/sources.list.d/rabbitmq.list
RUN wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | apt-key add -
RUN apt-get update
RUN apt-get install -y rabbitmq-server

# install sqlalchemy
RUN pip install sqlalchemy





#copy makefile
RUN mkdir -p /usr/ichnosat/server
COPY Makefile /usr/ichnosat
RUN export PYTHONPATH=${PYTHONPATH}:/usr/ichnosat
WORKDIR /usr/ichnosat/


#ENTRYPOINT [ "make" ]

