# The base image
FROM resin/rpi-raspbian

### Installation of dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y python
RUN apt-get install python-roslib
RUN apt-get install python-rospy
RUN apt-get install python-matplotlib
RUN apt-get install ros-std-msgs
RUN apt-get install ros-sensor-msgs
RUN pip install opencv-python
RUN pip install maths
RUN pip install numpy


# Installation of our program
COPY Lane-following.py /project/Lane-following.py
RUN chmod +x /project/Lane-following.py

# Setting the program as the default
CMD /usr/bin/python /project/Lane-following.py


