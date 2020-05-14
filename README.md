# UNDER CONSTRUCTIONS
# CarDetection---jetson

## The jetson will receive data from redis sent by multiple RPi with the following naming convention:

`imagedata_<pi_number>_<image_number>`

## The time is sent to redis with the following naming convention:

`time_<pi_number>_<image_number>`

## The accuracy and license plate is calculated with openalpr from the jetson

## Starting the redis server 
$ docker run --name <name of the container> -v ~/redis/redis.conf:/usr/local/etc/redis/redis.conf -d -p 0.0.0.0:6379:6379 --restart unless-stopped --network=host arm64v8/redis redis-server /usr/local/etc/redis/redis.conf


