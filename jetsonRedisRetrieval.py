import redis
from io import StringIO
from flask import send_file
import cv2
import numpy as np
import subprocess
import shlex
import sys
from shlex import quote
from datetime import datetime
import mysql.connector as mariadb

#r=redis.StrictRedis(host='192.168.1.110',password='nokia123')
r=redis.StrictRedis(host='localhost',password='project123')
r.set('numberOfPi', sys.argv[1])
imageCount = 0	#running variable for the images
Pi = list()	#list containing all the pi objects
location = "Some place"	# Dummy var, will be updated in the future	

class RPi:
	numberOfDevices = int(sys.argv[1])
	def __init__(self, ID, location):
		self.__ID = ID
		self.__Data_count = 0
		self.__Location = location
		self.__KeyPrefix = ('Pi%dimagedata' %self.__ID)
	def __del__(self):
		print("deleted")
	def nextImage(self):
		if (self.__Data_count < 100):
			self.__Data_count = self.__Data_count + 1
		else:
			self.__Data_count = 0
	def GetKey(self):
		return self.__KeyPrefix + ("%d" %self.__Data_count)
	def GetID(self):
		return self.__ID

"""
	Initialize the objects and save to the queue
	
	@param:	
		location: location of the pi
		
	@return:
		nothing
"""
def initialize():
	for i in range(RPi.numberOfDevices, 0, -1):
		dummyObj = RPi(i,location)
		Pi.append(dummyObj) 

def main():
	# Set up the pi and save the objects into a list
	initialize()
	cnt = 0
	while True:
		# Go through each obj of the list
		for i in range(RPi.numberOfDevices):
			# Create the key for the current pi
			key = Pi[i].GetKey()
			# Check if the key exist (the image has been sent to redis)
			if r.exists(key):
				img_bytes = r.get(key)	# Contains the value stored on redis (matrix containing the image data)
				# Decode the image data
				decoded = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), 1)
				cv2.imwrite("Output.jpg", decoded)
				
				# Evoking the shell alpr command
				file_ = open('plateResult.txt', 'w+')
				fileName = ('Output.jpg')
				command = './alpr.sh {}'.format(quote(fileName))
#				print(command)
				subprocess.call(shlex.split(command))
				file_.close()

				# Parsing the ouput file to read the data
				file_ = open('plateResult.txt', 'r+')
				line = file_.read()
				noPlate = "No license plates found."
				licensePlate = ""
				if noPlate in line:
					print("No plate found")
				else:
					licensePlate = line[line.find('- ')+2:line.find('c')-2]
#					print(licensePlate)
					accuracy = (line[line.find('.')-2:line.find('.')+3])
#					print("ACCURACY")
#					print(accuracy)
					file_.close()

				if licensePlate:
					# Connect to the php server and send the data to the correct tables
					mariadb_connection = mariadb.connect(host='localhost', user='DBinnovation', password='DBinnovation123', database='licenseDB')
					cursor = mariadb_connection.cursor()
					now = datetime.now()
#					print(now)
					timeRecord = now.strftime("%Y/%m/%d %H:%M:%S")
#					print("TIME RECORD")
#					print(timeRecord)
					cursor.execute("INSERT INTO records (licensePlate, timeStamp, accuracy, piID) VALUES (%s, %s, %s, %s)",(licensePlate, timeRecord, accuracy, Pi[i].GetID()))
					mariadb_connection.commit()
					cursor.close()
				else:
					print("seg. error")
				
				# Reset
				#r.delete(key)
				command = ""
				Pi[i].nextImage()


if __name__ == "__main__":
	main()
