# The base image
FROM resin/rpi-raspbian

### Installation of dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y python


# Installation of our program
COPY hello.py /project/hello.py
RUN chmod +x /project/hello.py

# Setting the program as the default
CMD /usr/bin/python /project/hello.py


