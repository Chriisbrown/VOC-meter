# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 11:14:21 2018

@author: chris
"""

#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.subscribe as subscribe
import pandas as pd
    
df = pd.DataFrame(columns=['Time','VOCs','eCO2','Temp'])
with open('homedata.csv', 'w+') as f:
        df.to_csv(f, header=True,index=False)
               
topics = ['#']
i = 0
N = 10000
while i < N:
    df_temp = pd.DataFrame(index=range(0,1), columns=['Time','VOCs','eCO2','Temp'])
    m = subscribe.simple(topics, hostname="10.0.100.130", retained=False, msg_count=4)
    for a in m:
        y = a.payload
        if a.topic == 'time':
            df_temp['Time'][0] = float(y.decode())
        if a.topic == 'VOCs':
            df_temp['VOCs'][0] = float(y.decode())
        if a.topic == 'eCO2':
            df_temp['eCO2'][0] = float(y.decode())
        if a.topic == 'Temp':
            df_temp['Temp'][0] = float(y.decode())
    print('message count:',i)
    df = df.append(df_temp)
    with open('homedata.csv', 'a+') as f:
        df_temp.to_csv(f, header=False)
    i += 1
    
print(df)
    
    