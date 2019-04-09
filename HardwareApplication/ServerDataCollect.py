
###################################################
# This script is used by Smart city system server #
# to perform the following operation:             #
#  1. Collect Smart city Sensor data              #
#  2. Update exsitng database with raw data entry #
###################################################

import mysql.connector
import socket
import pickle
import datetime

# Define PDU class
class PDU:
    def __init__(self, DeviceNum, DataType, Lat, Lng, Data, CollectTime):
        self.DeviceNum = DeviceNum
        self.DataType = DataType
        self.Lat = Lat
        self.Lng = Lng
        self.Data = Data
        self.CollectTime = CollectTime

# Configure socket info (host and port)
#host = '127.0.0.1'   # IP of the host
#host = '192.168.0.195'  # IP of host (Ethernet Static)
host = '192.168.0.105'
port = 12345

# Initialize socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))   # bind host and port to socket created

# Enable socket to listen for data (exactly 1 connection at a time
s.listen(5)   # limit to 5 at once

# Initialize SQL query statement
sqlQuery = "INSERT INTO sensordata (DeviceNumber, Lat, Lng, DataType, Data, CollectTime) VALUES (%s, %s, %s, %s, %s, %s)"

# Configure sql connection
mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "dumpstersite"
)

# Initializze database handle
dbcursor = mydb.cursor()

while True:
    # Wait and establish connection
    connection, address = s.accept()
    # Initilize new list variable for items to be added to database 
    val = []
    while True:
        rxData_Stream = connection.recv(1024)   # Listen and receive data
        if not rxData_Stream:
            # Exit receive loop from current connection
            connection.close()
            break
        # Re-construct PDU data from byte stream
        rxData = pickle.loads(rxData_Stream)
        # Add new value entry to be added
        val.append((rxData.DeviceNum, rxData.Lat, rxData.Lng, rxData.DataType, rxData.Data, rxData.CollectTime))

    # Insert new entries
    print(val)
    dbcursor.executemany(sqlQuery, val)
    mydb.commit()    # Commit/Execute SQL query
    print (dbcursor.rowcount, "was inserted")   # display # of inserted entry












