# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 11:14:21 2018

@author: chris
"""

#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.subscribe as subscribe
import matplotlib.pyplot as plt
import pandas as pd
    
df = pd.DataFrame(columns=['Time','VOCs','eCO2','Temp'])
with open('homedata.csv', 'w+') as f:
        df.to_csv(f, header=True,index=False)
        
f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
f.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

def plotting(axes,x,y,colour,label,ylabel):
    axes.clear()
    axes.plot(x,y,color=colour,label=label)
    axes.legend()
    axes.grid()
    axes.set_ylabel(ylabel)
    
       
topics = ['#']
i = 0
N = 10000
while i < N:
    df_temp = pd.DataFrame(index=range(0,1), columns=['Time','VOCs','eCO2','Temp'])
    m = subscribe.simple(topics, hostname="10.0.100.214", retained=False, msg_count=4)
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
        
    if i < 100:
        plotting(ax1,df['Time'], df['VOCs'],colour='red',label='VOCs',ylabel='ppb')
        plotting(ax2,df['Time'],df['eCO2'],colour='green',label='eCO2',ylabel='ppm')
        plotting(ax3,df['Time'],df['Temp'],colour='blue',label='Chip Temperature',ylabel='$^\circ$C')    
        ax3.set_xlabel('Time (s)')
        plt.pause(0.01)
        plt.show()
    else:
        plotting(ax1,df['Time'][i-100:i], df['VOCs'][i-100:i],colour='red',label='VOCs',ylabel='ppb')
        plotting(ax2,df['Time'][i-100:i],df['eCO2'][i-100:i],colour='green',label='eCO2',ylabel='ppm')
        plotting(ax3,df['Time'][i-100:i],df['Temp'][i-100:i],colour='blue',label='Chip Temperature',ylabel='$^\circ$C')    
        ax3.set_xlabel('Time (s)')
        plt.pause(0.01)
        plt.show()
    i += 1
    
print(df)
    
    
