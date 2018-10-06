FROM jamieleecho/coco-dev:0.10

MAINTAINER Jamie Cho version: 0.2

# Install image-magick
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y imagemagick
RUN apt-get clean

# Setup tools folder
ADD . /home/dynosprite/
WORKDIR /home/dynosprite/tools
RUN rm -f lwasm lwlink
RUN ln -s /usr/bin/lwasm .
RUN ln -s /usr/bin/lwlink .
WORKDIR ..
