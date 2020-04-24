###
# Testing class for the Jetson
# each raspberry pi is an object of the class, each with its own ip
###

class RPi:
    __username = ""
    __password = ""
    def __init__(self):
        __username = "DBinnovation"
        __password = "DBinnovation123"
    def connectToServer(self, username, password):    
        self.__username = username
        self.__password = password
    def sendToServer(self):
        mariadb_connection = mariadb.connect(host = 'localhost', user = self.__username, pasword = self.__password, database = 'licenseDB')
        cursor = mariadb_connection.cursor
        
        cursor.execute()
        mariadb_connection.commit()
        cursor.close()
        
    def getDataFromRedis(self, )
    def executeCommand(self, )
