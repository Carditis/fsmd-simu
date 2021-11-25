import machine
import network
import socket

ap = network.WLAN (network.AP_IF) #Creates access point. 
#We create an instance of the class WLAN. The access point allows other clients to connect to the wifi
ap.active (True) #Activates network interface
ap.config (essid = 'bestNet20') #essid = wifi access point name
ap.config (authmode = 3, password = 'supersejtpass') #

pins = [machine.Pin(i, machine.Pin.IN) for i in (16, 17, 21, 22, 23)] #we make the pins ready

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 Pins</title> </head>
    <body> <h1>ESP32 Pins</h1>
        <table border="1"> <tr><th>Pind</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1] #return a list of arrays, we take the last element in the first array

s = socket.socket() #creates a new socket
s.bind(addr)        #binds the socket to a specific address
s.listen(1)         #starts to listen on the socket

print('listening on', addr)
while True:
    cl, addr = s.accept()   #now we start to accept connections
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        print(line)
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]      #the pin values are read and updates the array
    response = html % '\n'.join(rows)                                                   #the array is concatenated with the html from line 13
    cl.send(response)                                                                   #now we send it
    cl.close()