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

ccs =  Adafruit_CCS811()

while not ccs.available():
	pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0

try:
    start_time = time.time()
    while(1):
        if ccs.available():
            temp = str(ccs.calculateTemperature())
            if not ccs.readData():
                x = str(ccs.getTVOC()) 
                y = str(ccs.geteCO2()) 
                with open('VOCdatainitial.txt' ,'a+') as f:
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
                with open('VOCdatabackup.txt' ,'a+') as f:
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
        
            
            
            
            

 
