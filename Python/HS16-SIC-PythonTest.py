#Vybe Python Example
#Haptics Symposium 2016 Student Innovation Challenge
#
# author: Oliver Schneider <oschneid@cs.ubc.ca>


#####################################
# Instructions
#
# 1. Plug in Vybe gaming chair (with customized firmware installed),
# turn it on, THEN connect USB to your computer.
#
# 2. Run this script
#
#####################################

import json
import serial #Requires PySerial
import serial.tools.list_ports
import time


#####################################
#
# Detect and Connect to Vybe Device
#
#####################################


#Load Vybe device details
vybe_desc = {}
with open('vybe.json', 'r') as f:
	vybe_desc = json.load(f)


#Search for all connected Vybe devices
connectedDevices = []
for portcandidate in serial.tools.list_ports.comports():
	# print portcandidate[2]
	port_type = portcandidate[2] #each port description is a list of length 3; item 3 has vendor id and product id
	# if port_type.find('USB VID:PID=%s:%d'%(str(vybe_desc["comm"]["usbserial"]["vid"]), vybe_desc["comm"]["usbserial"]["pid"])) >= 0:
	if port_type.find('USB VID:PID=0483:5740')>= 0:
		print "Found %s"%(portcandidate[0],)
		connectedDevices.append(portcandidate[0]) #name of this port

#Connect to first found Vybe device
vybe = None
if connectedDevices:
	portname = connectedDevices[0]
	vybe = serial.Serial(port=portname, baudrate=vybe_desc["comm"]["usbserial"]["baud"], writeTimeout = 0.05)
else:
	raise IOError("%s not detected."%(vybe_desc["name"],))



#####################################
#
# Functions for activating actuators
#
#####################################

def SetVoicecoil(index, value):
	# Set value to [0,255]
	value = min(max(0, value), 255)

	# format: "VCL <number as character> <buzz value 0-255 as character\n"
	msg = 	"VCL %s %s\n"%(str(index), chr(value))
	vybe.write(msg)
	vybe.flush()


def SetMotor(index, value):
	value = min(max(0, value), 255)

	# format: "MTR <number as character> <buzz value 0-255 as character\n"
	msg = 	"MTR %s %s\n"%(str(index), chr(value))
	vybe.write(msg)
	vybe.flush()

def waveMotor(index, value, T, dutyCycle):
	dutyCycle = min(max(0, dutyCycle), 1)

	# pull up
	SetMotor(index, value)
	time.sleep(T*dutyCycle)
	# pull down
	SetMotor(index, 0)
	time.sleep(T*(1-dutyCycle))

def waveVoicecoil(index, value, T, dutyCycle):
	dutyCycle = min(max(0, dutyCycle), 1)

	# pull up
	SetVoicecoil(index, value)
	time.sleep(T*dutyCycle)
	# pull down
	SetVoicecoil(index, 0)
	time.sleep(T*(1-dutyCycle))

def right(maxValue, T):
	coils = [3,[1,4],[2,5],6]
	value = maxValue
	for i in coils:
		if type(i) is not list:
			if i != 6:
				print i
				SetVoicecoil(i, value)
				time.sleep(T/4.)
				SetVoicecoil(i, 0)
			else:
				print i
				SetMotor(2, int(value*3.0/4))
				SetMotor(6, int(value*3.0/4))
				SetVoicecoil(i, value)
				time.sleep(T/2.)
				SetMotor(2, 0)
				SetMotor(6, 0)
				SetVoicecoil(i, 0)

		else:
			print i
			SetVoicecoil(i[0], value)
			SetVoicecoil(i[1], value)
			time.sleep(T/4.)
			SetVoicecoil(i[0], 0)
			SetVoicecoil(i[1], 0)
		

#####################################
#
# Buzz actuators
#
#####################################

# for i in xrange(5):
# 	right(255, 0.5)
# 	time.sleep(0.5)

# for i in xrange(50):
# 	waveVoicecoil(6,255*(49-i)/49,0.2,0.5)
# 	print i

buzz_intensity = 255 #can send a value from 0 to 255
buzz_duration = 1 #second


#Buzz each voice coil (numbered 1-6)
for i in range(1,7):
	SetVoicecoil(i, buzz_intensity)
	time.sleep(buzz_duration)
	SetVoicecoil(i, 0)


#Buzz each rumble motor (numbered 1-6)
for i in range(1,7):
	SetMotor(i, buzz_intensity)
	time.sleep(buzz_duration)
	SetMotor(i, 0)


#Buzz all actuators at once
for i in range(1,7):
	SetVoicecoil(i, buzz_intensity)
	SetMotor(i, buzz_intensity)
time.sleep(buzz_duration)
for i in range(1,7):
	SetVoicecoil(i, 0)
	SetMotor(i, 0)

