# CarDetection---jetson
This is an innovation project of Students from Metropolia University of Applied Sciences, working in collaboration with NOKIA.  
The goal of this project is to create a modular systems of IoT devices for license plate recognition. Each module consists of a Raspberry Pi 3B+, equipped with a Pi Noir camera module to record live video feed and detect vehicles. Once having identify vehicles and finished pre-processing, the frames are sent the the master module consisting of a single Jetson Nano via Redis, for lincense plate recognition. The final data is then cross-checked with an online database for further applications

This repository contains all the materials needed for the Jetson Nano, which includes:
1. The redis server hosting instruction
2. The files needed for data retrival, image processing and sending data to the cloud

## Setting up the redis server
### Install docker
1. Download the script from docker.com and run it  
>`$ curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh`  

(Opional): Add the user to the newly minted docker group. This will enable running docker commands without using sudo
>`$ sudo usermod -aG docker pi`  

Issue the following command to avoid having to log out and log back in for the docker group change to take effect
>`$ newgrp docker`
2. Verify the success of the installation by checking the docker version  
>`$ docker --version`  

A better test can be carried out by creating a docker container from the hello-world image  
>`$ docker run hello-world`

### Install redis from Docker image
As noted on the Redis administration page, it's a good idea to set the Linux kernel overcommit memory setting to 1. This helps in scenarios such as memory allocation during the background saving of the Redis database.  
1. Update Linux kernel overcommit memory setting  
>`$ sudo nano /etc/sysctl.conf`

2. Add the following to the bottom of the file:
>`vm.overcommit_memory = 1`

3. Determine the Redis version we'll be containerizing. The version used in this project is 6.0.1  
The Versions can be check from the [arm64v8/redis dockerhub page](https://hub.docker.com/r/arm64v8/redis/)

4. Create a directory for the Redis configuration file and download the coresponding version 
>`$ mkdir ~/redis`  
>`$ REDIS_VERSION=6.0.1`  
>`$ curl -O https://raw.githubusercontent.com/antirez/redis/$REDIS_VERSION/redis.conf`

5. Edit the redis.conf file
>`$ nano redis.conf`  
Modify/add the following:
- bind 0.0.0.0
- tcp-backlog 128
- requirepass <your password> (Optional)
- maxmemory 512mb
- appendonly yes
  
6. Create the Redis container
>`$ docker run --name <name of the container> -v ~/redis/redis.conf:/usr/local/etc/redis/redis.conf -d -p 0.0.0.0:6379:6379 --restart unless-stopped --network=host arm64v8/redis redis-server /usr/local/etc/redis/redis.conf`

### Install redis-cli client (redis command line interface)
This part is optional as it provides a way of verifying connection and data integrity. We can use this to send commands to Redis server and read the replies.
>`$ sudo apt install redis-tools`  

Once finished, the redis-cli interface can be accessed with:  
>`$ redis-cli`
### Some useful commands to test the redis server
1. Use the command line interface to connect to a server hosted on a different machine on the same network  
>`redis-cli -h <host ip address>`

2. If the server is configured with a password, use  
>`auth <your password>`

The server can also be directly accessed (even with a password) with the argument "-a"
>`redis-cli -a <your password>`

3. Set a key with a value  
>`set <KEY> <VALUE>`

4. Check the value of a key  
>`get <KEY>`

5. Check for the existance of multiple keys  
>`KEYS *`

6. Clear all set keys  
>`FLUSHDB`

This README is written with reference to [this guide](https://thisdavej.com/how-to-install-redis-on-a-raspberry-pi-using-docker/) on installing redis on the raspberry pi, with minor adjustments to accomodate the hardware and software difference

### Running the script
Run the shell script start.sh, providing the number of Raspberry Pi expected in the current system  
>`./start.sh <number of pi>`

### Notes 
The OpenALPR library handles most of the work identifying licence plates. The communication and naming convention are pre-coded and follow the following guidelines:  
1. The KEY to the image data is formatted as:  
>`Pi<Pi ID>imagedata<Image data >`
