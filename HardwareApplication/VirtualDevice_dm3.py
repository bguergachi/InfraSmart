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
    dataType = "Grabage(ultrasonic)"
    maxCapacity = 0
    binUsage = 0

    # Instance Attribute (Initialization)
    def __init__(self, deviceID, Lng, Lat):
        self.deviceID = deviceID
        self.Lng = Lng
        self.Lat = Lat

    #Instance Method
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

    # Instance Method
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
        return()
# }}}
# {{{ [CLASS] PDU
class PDU:

    def __init__ (self, DeviceNum, DataType, Lat, Lng, Data, CollectTime):
        self.DeviceNum = DeviceNum
        self.DataType = DataType
        self.Lat = Lat
        self.Lng = Lng
        self.Data = Data
        self.CollectTime = CollectTime
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

# Add device detail to device list (default = 9)
devices.append(VirtualDevice("1001", 43.65204426, -79.40361049))
devices.append(VirtualDevice("1002", 42.64582615, -79.46744499))
devices.append(VirtualDevice("1003", 43.67188004, -79.38909398))
devices.append(VirtualDevice("1004", 43.65591903, -79.39342123))
devices.append(VirtualDevice("1005", 43.67084828, -79.36808013))
devices.append(VirtualDevice("1006", 43.67209961, -79.38603076))
devices.append(VirtualDevice("1007", 43.66110569, -79.37084870))
devices.append(VirtualDevice("1008", 43.65184241, -79.38645152))
devices.append(VirtualDevice("1009", 43.64631791, -79.36521410))


# Calibrate each device using single ultrasonic sensor
for i in range (0, len(devices)):
    devices[i].calibrate(TRIG, ECHO)
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
        devices[i].updateBinData(TRIG, ECHO, 8)
        print ("OK[%.2f]" % devices[i].binUsage);
	# Add current result to Sensor data array
        SensorData.append(PDU(devices[i].deviceID, devices[i].dataType, devices[i].Lat, devices[i].Lng, devices[i].binUsage, datetime.datetime.now()))
    loopCounter = loopCounter - 1
print ("\n")

# }}}

# {{{ Sending Sensor data to server device

# Send data to Smart City server
print ("[SYS] Sending Data to Server...")

# Configure socket (host + port)
print ("    Configuring socket..."),
host = '192.168.0.231'   # IP of server
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


