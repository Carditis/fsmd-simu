# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 18:24:35 2021

@author: emilp
"""
import socket
import time 
from datetime import datetime
import csv

i=0
while True:
    request = b"GET / resources/temp\r\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect(("192.168.4.1", 80)) 
    s.settimeout(2) 
    s.send(request) 
    
    try: 
        result = s.recv(10000) 
        while (len(result) > 0): 
            #print(result) 
            x = str(result)
            result = s.recv(10000) 
    except: 
        pass 
    
    s.close() 
    
    x = x.replace("\\","")
    x = x[2:-1]
    temp = float(x[13:-1])
    y = str(datetime.now())[:-7]
    row = [y, i, temp]
    
    f = open('C:/Users/emilp/Desktop/cyber server csv/Temps.csv', 'a')
    writer = csv.writer(f, delimiter=',', lineterminator='\n')
    writer.writerow(row)
    f.close
    
    i = i + 1
    time.sleep(2)