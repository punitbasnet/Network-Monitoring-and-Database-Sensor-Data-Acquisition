#!/etc python3

import time
import serial
import RPi.GPIO as gpio
import threading
import datetime
import hashlib
import hmac


#calibrate cond before deployment

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(24, gpio.OUT) #this is x and pin 18
gpio.setup(23, gpio.OUT) #this is y and pin 16

#date = datetime.datetime.now().strftime("%Y-%m-%d")

def calibration():
 global rtemp
 calitime = datetime.datetime.now().strftime("%H:%M:%S")
 ser.write("T,{}\r".format(rtemp).encode('ascii'))
 time.sleep(.5)
 a = ser.readline().decode('ascii')
 calresult = 0
 #print("attemped calibration")
 if ("OK") in a:
  calresult = 1
 return(calitime,calresult)

def getreadings():
 global rtemp, date
 calresult = 0
 count = 0
 threading.Timer(600.0, getreadings).start()
 current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 date = datetime.datetime.now().strftime("%Y-%m-%d")
 #ut=time.mktime(datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S").timetuple())
 #print(date)
 f = open('/home/pi/readings/normalreadings/current/readings_{}.txt'.format(date),'a')
 fhmac = open('/home/pi/readings/hmacs/current/hmacreadings_{}.txt'.format(date),'a')
 
#HMAC_create portion ------------------------------------------------------------

 Loc = "Baker"
 bLoc=Loc.encode()
 LocID = "39.326265,-82.103506"
 bLocID = LocID.encode()
 pwd=b"sensor"
 salt=bLoc+bLocID
 keylength = 12
 NumKDHashes = 10000
 key = hashlib.pbkdf2_hmac('sha256', pwd, salt, NumKDHashes, dklen=keylength)


#temperature -----------------------------------------------------------------
 x=1
 y=0
 gpio.output(24, x)
 gpio.output(23, y)
 ser.flushInput()
 time.sleep(.5)
 ser.write("r\r".encode("ascii"))
 time.sleep(.5)
 s = ser.readline().splitlines()
 rtemp = s[0].decode('ascii')
 ser.flushOutput()
 time.sleep(.5)
 while (ser.readline() != b''):
  ser.flushInput()

#Conductivity ----------------------------------------------------------------
 x=0
 y=1
 gpio.output(24, x)
 gpio.output(23, y)
 ser.flushInput()
 time.sleep(.5)
 ser.write("r\r".encode("ascii"))
 time.sleep(.5)
 s = ser.readline().splitlines()
 rcon = s[0].decode('ascii')
 while (ser.readline() != b''):
  ser.flushInput()

#Reading collection ------------------------------------------------------
 r = "Baker {} Temperature {} Conductivity {}".format(current_time, rtemp, rcon)
 rhmac = hmac.new(key, (r+"\n").encode(), hashlib.sha256).hexdigest()
 
 f.write(r)
 f.write("\n")
 fhmac.write(rhmac)
 fhmac.write("\n")
 
 print("sensor data logged at {}".format(current_time))
 

#Temperature Compensation ----------------------------------------------------------------
 
 ser.write("T,?\r".encode("ascii"))
 time.sleep(.5)
 c = ser.readline().splitlines()[0].decode('ascii')
 cali = c.split(",",1)[1]
 frtemp = float(rtemp)
 fcali = float(cali)
 #print(fcali)
 #print("temp {}".format(frtemp))
 if (abs(frtemp-fcali) > 2):   #and abs(frtemp-fcali) < 6):
  while(calresult == 0):
   (calitime, calresult) = calibration()
   count += 1
   if (count == 3):
    rcom = "Compensation was unsuccessful at {}".format(calitime)
    rcomhmac = hmac.new(key, (rcom+"\n").encode(), hashlib.sha256).hexdigest()
    #com = 'Zabbix_Server comp {} "Compensation Unsuccessful"'.format(ut)
    #comhmac = hmac.new(key, (com+"\n").encode(), hashlib.sha256).hexdigest()
    f.write(rcom)
    fhmac.write(rcomhmac)
    f.write("\n")
    fhmac.write("\n")
 #   ihmac.write("\n")
    break
   if (calresult == 1):
    rcom= "Conductivity sensor compensated at {} with temperature value {}".format(calitime, rtemp)
    rcomhmac = hmac.new(key, (rcom+"\n").encode(), hashlib.sha256).hexdigest()
    #com = 'Zabbix_Server comp {} "Compensation Successful"'.format(ut)
    #comhmac = hmac.new(key, (com+"\n").encode(), hashlib.sha256).hexdigest()
    f.write(rcom)
    fhmac.write(rcomhmac)
    f. write("\n")
    fhmac.write("\n")
    
    #ihmac.write("\n")
 print("HMAC at {}".format(current_time))
 f.close()
 fhmac.close()
 #g.close
 #h.close
 #i.close

ser = serial.Serial(
 	port="/dev/ttyAMA0",
 	baudrate = 9600,
 	parity=serial.PARITY_NONE,
 	stopbits=serial.STOPBITS_ONE,
 	bytesize=serial.EIGHTBITS,
 	timeout=1
)

ser.flushInput()
ser.flushOutput()
x=0
y=0

gpio.output(24, x)
gpio.output(23, y)

rtemp = "temp"
getreadings()
