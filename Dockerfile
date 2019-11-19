# The base image
FROM resin/rpi-raspbian

### Installation of dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install opencv-python
RUN pip install maths
RUN pip install numpy
RUN pip install matplotlib
RUN pip install rospy
RUN pip install roslib


# Installation of our program
COPY Lane-following.py /project/Lane-following.py
RUN chmod +x /project/Lane-following.py

# Setting the program as the default
CMD /usr/bin/python /project/Lane-following.py


