import socket
import time 

request = b"GET / resources\r\n"
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
