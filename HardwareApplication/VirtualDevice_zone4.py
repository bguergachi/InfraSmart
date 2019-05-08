#############################################################################
#  This is a sample code generated for demo #1 of smart city EDP to create
#  create virtual devices that share a single sensor (ultrasonic) and 
#  simply display the data in the terminal indicating it's availability.
#############################################################################

import RPi.GPIO as GPIO   # import raspberry pi GPIO library
import time               # import time library
import datetime		  # import datetime library
import socket		  # import socket library
import pickle		  # import picle library

# Set gpio mode
GPIO.setmode(GPIO.BCM)

# {{{ [CLASS] VirtualDevice
# Define class for virtual devices
class VirtualDevice:

    # Class Attribute
    dataType = "Dumpster"
    maxCapacity = 0
    binUsage = 0

    # Instance Attribute (Initialization)
    def __init__(self, deviceID, Lng, Lat, Addr):
        self.deviceID = deviceID
        self.Lng = Lng
        self.Lat = Lat
        self.Addr = Addr

    #Instance Method
    # {{{ calibrate(self, trig, echo)
    def calibrate(self, trig, echo):
        #Specify calibrate accuracy
        total = 0
        count = 10
        while (count > 0):
	    #Toggle input pin to initiate reading
            GPIO.output(trig, True)
            time.sleep(0.00001)
            GPIO.output(trig,False)
            #GetStartAndEndTime
            while GPIO.input(echo)==0:
                pulse_start = time.time()
            while GPIO.input(echo)==1:
                pulse_end = time.time()
            #Calculate bin reading
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance,2)
            total = total + distance
            #Wait before proceed with next reading
            time.sleep(0.3)
            #Decrement count
            count = count - 1
        # Get averaged reading
        self.maxCapacity = total/10
        #print (self.maxCapacity)
        return()
    # }}}

    #Instance Method
    def setMaxCapacity(self, maxCap):
        self.maxCapacity = maxCap
        return()

    # Instance Method
    # {{{ updateBinData(self, trig, echo, sample)
    def updateBinData(self, trig, echo, sample):
        total = 0
        count = sample
        while(count != 0):
	    #Toggle input pin to initiate reading
            GPIO.output(trig, True)
            time.sleep(0.00001)
            GPIO.output(trig,False)
            #GetStartAndEndTime
            while GPIO.input(echo)==0:
                pulse_start = time.time()
            while GPIO.input(echo)==1:
                pulse_end = time.time()
            #Calculate bin reading
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance,2)
            total = total + distance
            #Display reading
            #print ("Distance: ",distance,"cm")
            print ('.', end="", flush=True),
            #Wait before proceed with next reading
            time.sleep(0.3)
            #Decrement count
            count = count - 1
        # Get averaged reading
        self.binUsage = 100*(self.maxCapacity - total/sample)/self.maxCapacity
        self.binUsage = -1*self.binUsage if self.binUsage < 0 else self.binUsage
        # Limit max bid data to 100
        if self.binUsage > 1:
            self.binUsage = 1

        return()
    # }}}

    # Instance Method
    def setBinData(self, binDat):
       
        offset = 0 
        # Offset data for demo
        binDat = binDat + offset
        # Limit max bid data to 100
        if  binDat > 1:
            binDat = 1
        self.binUsage = binDat
        return()
# }}}
# {{{ [CLASS] PDU
class PDU:

    def __init__ (self, DeviceNum, DataType, Lat, Lng, Addr, Data, CollectTime):
        self.DeviceNum = DeviceNum
        self.DataType = DataType
        self.Lat = Lat
        self.Lng = Lng
        self.Addr = Addr
        self.Data = Data
        self.CollectTime = CollectTime
# }}}

# {{{ [Function] getMaxCap
def getMaxCap(trig, echo):
    #Specify calibrate accuracy
    total = 0
    count = 10
    while (count > 0):
        #Toggle input pin to initiate reading
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig,False)
        #GetStartAndEndTime
        while GPIO.input(echo)==0:
            pulse_start = time.time()
        while GPIO.input(echo)==1:
            pulse_end = time.time()
        #Calculate bin reading
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance,2)
        total = total + distance
        #Wait before proceed with next reading
        time.sleep(0.3)
        #Decrement count
        count = count - 1
    # Get averaged reading
    return total/10
# }}} 
# {{{ [Function] getBinData
def getBinData(trig, echo, sample, maxCapacity):
    total = 0
    count = sample
    while(count != 0):
        #Toggle input pin to initiate reading
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig,False)
        #GetStartAndEndTime
        while GPIO.input(echo)==0:
            pulse_start = time.time()
        while GPIO.input(echo)==1:
            pulse_end = time.time()
        #Calculate bin reading
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance,2)
        total = total + distance
        #Display reading
        #print ("Distance: ",distance,"cm")
        print ('.', end="", flush=True),
        #Wait before proceed with next reading
        time.sleep(0.3)
        #Decrement count
        count = count - 1
    # Get averaged reading
    binData = 1*(maxCapacity - total/sample)/maxCapacity
    binData = -1*binData if binData < 0 else binData
    print("{%.4f} " %maxCapacity, end ="", flush=True)
    print("{%.2f} " %binData, end="", flush=True)
    return binData

# }}}

# Setup Ultrasonic sensor
TRIG = 23
ECHO = 24
#Configure GPIO Pin
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
#Allow output to settle
GPIO.output(TRIG, False)
time.sleep(2)   #wait for sensor to settle

# {{{ Initialize Virtual device configuration

# Generate virtual device
devices = []
print ("[SYS] Initialize Virtual devices...")

# Add device detail to device list
# NOTE: Locations specified are for zone 1
# VirtualDevice( ID#, Longtitude, Latitude)
devices.append(VirtualDevice("1031", -79.389412, 43.64038,"305 Bremner Bldvd, Toronto ON"))
devices.append(VirtualDevice("1032", -79.39160915, 43.6490511,"296 Richmond St W, Toronto ON M5V 1X2"))
devices.append(VirtualDevice("1033", -79.38058295, 43.64964313,"320-298 Bay St, Toronto ON M5H 4A6"))
devices.append(VirtualDevice("1034", -79.3782348, 43.66585814,"67-89 Bond St, Toronto ON"))
devices.append(VirtualDevice("1035", -79.38304921, 43.65099757,"15-26 The path (Victory-Federal Bldg), Toronto ON"))
devices.append(VirtualDevice("1036", -79.38084584, 43.64978933,"320 Bay St, Toronto ON M5H 4A6"))
devices.append(VirtualDevice("1037", -79.378096, 43.64160619,"20 Bay St, Toronto ON M5J 2N8"))
devices.append(VirtualDevice("1038", -79.38793473, 43.64125606,"CityPlace Toronto ON"))
devices.append(VirtualDevice("1039", -79.367528, 43.650489,"176 Front St E, Toronto ON"))
devices.append(VirtualDevice("1040", -79.394309, 43.643412,"28-24 Spadina Avenue, Toronto ON"))


# Calibrate each device using single ultrasonic sensor
binMaxCap = getMaxCap(TRIG, ECHO)
for i in range (0, len(devices)):
    #devices[i].calibrate(TRIG, ECHO)
    devices[i].setMaxCapacity(binMaxCap)
    print ("Device '",devices[i].deviceID,"' setup complete")
print ("\n")

# }}}

# {{{ Process Garbage collction data collection

# Setup device data collection
print ("[SYS] Begin Data collection...")
SensorData = []    # Initialize array for data collection
loopCounter=1      # Set number of iteration to collect info (default = 1)
while (loopCounter > 0):
    for i in range (0, len(devices)):
	# Display status message for devie data collection
        print ("    Device#",devices[i].deviceID, end="", flush=True)
	# Update bin content
        #devices[i].updateBinData(TRIG, ECHO, 8)
        binData = getBinData(TRIG, ECHO, 8, devices[i].maxCapacity)
        devices[i].setBinData(binData)
        print ("OK[%.2f]" % devices[i].binUsage);
	# Add current result to Sensor data array
        SensorData.append(PDU(devices[i].deviceID, devices[i].dataType, devices[i].Lat, devices[i].Lng, devices[i].Addr, devices[i].binUsage, datetime.datetime.now()))
    loopCounter = loopCounter - 1
print ("\n")

# }}}

# {{{ Sending Sensor data to server device

# Send data to Smart City server
print ("[SYS] Sending Data to Server...")

# Configure socket (host + port)
print ("    Configuring socket..."),
#host = '192.168.0.231'   # IP of server
#host = '192.168.0.104'   #IP for James PC server
host = '192.168.0.105'   #IP for Adam PC server
port = 12345         # Port to use for server connection
print("OK")

# Initialize socket
#print ("    Initialize client socket..."),
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((host, port))
#print ("OK")

# Send out each entry individually
print ("    Sending Data...")
for i in range(0, len(SensorData)):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print (host)
    print (port)
    s.connect((host, port))
    print(SensorData[i])
    #txData = PDU (SensorData[i])
    txData = SensorData[i]
    txDataStream = pickle.dumps(txData, protocol=2)
    s.send(txDataStream)
    s.close()

#print ("Complete.")
print ("\n")

# }}}

# {{{ Display data collection result
# Display loop result
print ("[SYS] Display Loop result...")
print ("DeviceID    Type      Longitude   Latitude       BinUsage")
for i in range (0, len(devices)):
    print (devices[i].deviceID,"    ",devices[i].dataType," ",devices[i].Lng,devices[i].Lat,"  %.2f %%" % devices[i].binUsage)
loopCounter = loopCounter - 1

# }}}

# Reset GPIO pin
GPIO.cleanup()


