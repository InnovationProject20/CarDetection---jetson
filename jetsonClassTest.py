###
# Testing class for the Jetson
# each object of the class process data from a different pi, each with its own ip
###

class RPi:
    __username = ""     #username for the php server
    __password = ""     #password for the php server
    __ID = ""           #ID of the pi (initiated value)
    __Data_count = ""   #The number of the photo from a pi (incremented value)
    __r = ""            #redis object
    __plate = ""        #the plate from the picture
    __accuracy = ""     #accuracy
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
    #def executeCommand(self)
