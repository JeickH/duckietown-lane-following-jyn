# Simple program to run via Docker

As explained [in the guide](http://docs.duckietown.org/DT18/opmanual_duckiebot/out/docker_setup.html), 
these commands need to be run from your laptop, but things will happen on the robot.

First clone the repo:
    
    $ git clone https://github.com/duckietown/rpi-duckiebot-simple-python.git
    $ cd rpi-duckiebot-simple-python

Run the following:

    $ docker -H <YOUR_DUCKIEBOT>.local  build -t my-simple-python-program .
    
The docker daemon on the Duckiebot will build the container.

Then run the following:

    $ docker -H <YOUR_DUCKIEBOT>.local  run -it --network=host my-simple-python-program

You should see this output:

    I am executing on the host <HOSTNAME>



**Note**: If you set the variable `DOCKER_HOST` as:

    export DOCKER_HOST=<YOUR_DUCKIEBOT>.local

then you can avoid `-H <YOUR_DUCKIEBOT>.local`.
