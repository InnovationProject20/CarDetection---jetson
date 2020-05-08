import redis
from io import StringIO
from flask import send_file
import cv2
import numpy as np
import subprocess
import shlex
from shlex import quote
from datetime import datetime
import mysql.connector as mariadb

#r=redis.StrictRedis(host='192.168.1.110',password='nokia123')
r=redis.StrictRedis(host='localhost',password='project123')
imageCount = 0

while (imageCount < 5):
	img_bytes = r.get('imagedata%d' %imageCount)
	if (img_bytes):
		decoded = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), 1)
		cv2.imwrite("retTest%d.jpg" %imageCount, decoded)
		# Evoking the shell alpr command
		file_ = open('plateResult.txt', 'w+')
		fileName = ('retTest%d.jpg' %imageCount)
		command = './alpr.sh {}'.format(quote(fileName))
		print(command)
		subprocess.call(shlex.split(command))
		file_.close()
		# Parsing the ouput file to read the data
		file_ = open('plateResult.txt', 'r+')
		line = file_.read()
		licensePlate = line[line.find('- ')+2:line.find('c')-2]
		print(licensePlate)
		accuracy = float(line[line.find(".")-2:line.find('.')+3])
		print("ACCURACY")
		print(accuracy)
		file_.close()

		mariadb_connection = mariadb.connect(host='localhost',user='DBinnovation',password='DBinnovation123',database='licenseDB')
		cursor = mariadb_connection.cursor()
		now = datetime.now()
		print(now)
		timeRecord = now.strftime("%Y/%m/%d %H:%M:%S")
		print("TIME RECORD")
		print(timeRecord)
		cursor.execute("INSERT INTO records (licensePlate, timeStamp, accuracy) VALUES (%s, %s, %s)",(licensePlate, timeRecord, accuracy))
		mariadb_connection.commit()
		cursor.close()

		command = ""
		imageCount +=1
	#else:
		#print("no image\r\n")


class RPi:
    __username = ""     #username for the php server
    __password = ""     #password for the php server
    __ID = ""           #ID of the pi (initiated value)
    __Data_count = ""   #The number of the photo from a pi (incremented value)
    __r = ""            #redis object
    def __init__(self, ID):
        __username = "DBinnovation"
        __password = "DBinnovation123"
        __r = gRedis
        __ID = ID
        __Data_count = 0
    def connectToServer(self, username, password):    
        self.__username = username
        self.__password = password
    def sendToServer(self):
        mariadb_connection = mariadb.connect(host = 'localhost', user = self.__username, pasword = self.__password, database = 'licenseDB')
        cursor = mariadb_connection.cursor
        
        # Open alpr output file
        file = open("plateResult","r+")
        # Parse to get the first result of plate and accuracy
        line = file.read()
        licensePlate = line[line.find('- ')+2:line.find('c')-2]
        accuracy = float(line[line.find(".")-2:line.find('.')+3])
        file.close()
        now = datetime.now()
        timeRecord = now.strftime("%d/%m/%Y %H:%M:%S")
        # Send to the PHP server
        cursor.execute()
        #cursor.execute("INSERT INTO records (licensePlate, timeRecord, Accuracy) VALUES ()))
        mariadb_connection.commit()
        cursor.close()
        
    def getDataFromRedis(self, r)
        img_bytes = r.get('imagedata_%d_%d',%self.__ID, %self.__Data_count)
        if (img_bytes):
            decoded = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), 1)
            cv2.imwrite("retTest_%d_%d.jpg", %self.__ID, %self.__Data_count, decoded)
            
            fileName = ('retTest_%d_%d', %self.__ID, %self.__Data_count)
            command = './alpr.sh {}'.format(quote(fileName))
            print(command)
            subprocess.call(shlex.split(command))
            command = ""
            self.__Data_count+=1
