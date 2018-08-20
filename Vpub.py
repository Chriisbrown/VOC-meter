# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 12:12:21 2018

@author: chris
"""

import paho.mqtt.publish as publish

MQTT_SERVER = "10.0.100.214"
MQTT_PATH = "time"
MQTT_PATH2 = "VOCs" 
MQTT_PATH3 = "eCO2"
MQTT_PATH4 = "Temp"

import time
from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811

def inputno(g, a, lim1, lim2):
#This defines the function used to check user inputs are within range and of correct data type
    if g == 1:
        while True:
            try:
                h = int(input(a))
                if lim1 <= h <= lim2:
                    return h
                else:
                    time.sleep(0.033)
            except ValueError:
                time.sleep(0.033)
                continue
#If a wrong value is entered the Red LED will flash

ccs =  Adafruit_CCS811()

while not ccs.available():
	pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0

Menu = '0'
while Menu != 'q':
    Menu = input('Press 1 to begin log, press q to quit: ')
#Menu setup allowing the program to be run multiple times without turning the pi off
    now = datetime.datetime.now()
    if Menu == '1':
        frequency = inputno(1,'Frequency of data reading: ',1,100)
        length = int((inputno(1,'Run test for how many minutes: ',1,1500))*60/frequency)
#All relevant parameters, with incorrect user input checking
        i = 0
        start_time = time.time()
	try:
	    while(1):
		if ccs.available():
		    temp = str(ccs.calculateTemperature())
		    if not ccs.readData():
			x = str(ccs.getTVOC()) 
			y = str(ccs.geteCO2()) 
			with open('VOCdatainitial'+now.strftime("%Y-%m-%d %H-%M")+'.txt' ,'a+') as f:
			    t = str(time.time() - start_time) 
			    s = t + ' ' + x + ' ' + y + ' ' + temp
			    print s
			    print >>f, s

			msgs = [{'topic':MQTT_PATH2, 'payload':x},(MQTT_PATH3,y,0,False),(MQTT_PATH4,temp,0,False),(MQTT_PATH,t,0,False)]
			publish.multiple(msgs,hostname=MQTT_SERVER)

		    else:
			publish.single("ERROR", hostname=MQTT_SERVER)
			while(1):
			    pass
		sleep(5)
	    f.close() 

	except:
	    print 'Time files when you\'re having fun'
	    while(1):
		if ccs.available():
		    temp = str(ccs.calculateTemperature())
		    if not ccs.readData():
			x = str(ccs.getTVOC()) 
			y = str(ccs.geteCO2()) 
			with open('VOCdatabackup'+now.strftime("%Y-%m-%d %H-%M")+'.txt'' ,'a+') as f:
			    t = str(time.time() - start_time) 
			    s = t + ' ' + x + ' ' + y + ' ' + temp
			    print s
			    print >>f, s

		    else:
			print 'no'
			while(1):
			    pass
		sleep(5)
	    f.close()
        
            
            
            
            

 
