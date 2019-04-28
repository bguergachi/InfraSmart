
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

# {{{ Define PDU class
class PDU:
    def __init__(self, DeviceNum, DataType, Lat, Lng, Addr, Data, CollectTime):
        self.DeviceNum = DeviceNum
        self.DataType = DataType
        self.Lat = Lat
        self.Lng = Lng
        self.Addr = Addr
        self.Data = Data
        self.CollectTime = CollectTime
# }}}

# Configure socket info (host and port)
#host = '127.0.0.1'   # IP of the host
#host = '192.168.0.195'  # IP of host (Ethernet Static)
#host = '192.168.56.1'
host = '192.168.0.104'
port = 12345

# Initialize socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))   # bind host and port to socket created

# Enable socket to listen for data (exactly 1 connection at a time
s.listen(5)   # limit to 5 at once

# Initialize SQL query statement
#sqlQuery = "INSERT INTO sensordata (DeviceNumber, Lat, Lng, DataType, Data, CollectTime) VALUES (%s, %s, %s, %s, %s, %s)"
zoneSqlQuery = "INSERT INTO sensordata (DeviceNumber, Lat, Lng, Address, DataType, Data, CollectTime) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#mainSqlQuery = "INSERT INTO sensordata (DeviceNumber, Lat, Lng, Address, DataType, Data, CollectTime) VALUES (%s, %s, %s, %s, %s, %s, %s)"
mainSqlQuery = "UPDATE sensordata SET Lat=%s, Lng=%s, Address=%s, DataType=%s, Data=%s, CollectTime=%s WHERE DeviceNumber=%s"

while True:
    
    # Wait and establish connection
    connection, address = s.accept()
    # Initilize new list variable for items to be added to database 
    val1 = []
    val2 = []

    while True:
        rxData_Stream = connection.recv(1024)   # Listen and receive data
        if not rxData_Stream:
            # Exit receive loop from current connection
            connection.close()
            break
        # Re-construct PDU data from byte stream
        rxData = pickle.loads(rxData_Stream)
        # Update value vector with data to be added
        #val.append((rxData.DeviceNum, rxData.Lat, rxData.Lng, rxData.DataType, rxData.Data, rxData.CollectTime))
        val1.append((rxData.DeviceNum, rxData.Lat, rxData.Lng, rxData.Addr, rxData.DataType, rxData.Data, rxData.CollectTime))
        val2.append((rxData.Lat, rxData.Lng, rxData.Addr, rxData.DataType, rxData.Data, rxData.CollectTime, rxData.DeviceNum)) 

    # {{{ Connection to zone data base for info storage
    if int(rxData.DeviceNum) >= 1001 and int(rxData.DeviceNum) <= 1010:
        zone = 'zone_1'
    elif int(rxData.DeviceNum) <=1020:
        zone = 'zone_2'
    elif int(rxData.DeviceNum) <=1030:
        zone = 'zone_3'
    elif int(rxData.DeviceNum) <=1040:
        zone = 'zone_4'
    else:
        zone = 'zone_undef'
    # Configure sql connection
    zonedb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = zone
    )
    # Initializze database handle
    zcursor = zonedb.cursor()
    # Insert new entries
    print(zoneSqlQuery)
    print(val1)
    zcursor.executemany(zoneSqlQuery, val1)
    zonedb.commit()    # Commit/Execute SQL query
    # Close cursor and db handle
    zcursor.close();
    zonedb.close();
    # }}}

    # {{{ Connect to main database for info storage
    
    # Configure sql connection
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "smart_city_main"
    )
    # Initializze database handle
    dbcursor = mydb.cursor()
    # Insert new entries
    print(mainSqlQuery)
    print(val2)
    dbcursor.executemany(mainSqlQuery, val2)
    mydb.commit()    # Commit/Execute SQL query
    print (dbcursor.rowcount, "was inserted")   # display # of inserted entry
    # Close cursor and db handle
    dbcursor.close();
    mydb.close();

    # }}}











