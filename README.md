# CarDetection---jetson

## The jetson will receive data from redis sent by multiple RPi with the following naming convention:

`imagedata_<pi_number>_<image_number>`

## The time is sent to redis with the following naming convention:

`time_<pi_number>_<image_number>`

## The accuracy and license plate is calculated with openalpr from the jetson
