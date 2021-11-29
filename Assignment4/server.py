import machine
import network
import socket
"""import time
data = bytearray(2)
i2c = machine.I2C(scl=machine.Pin(22),sda=machine.Pin(23))
address = 24
temp_reg = 5
res_reg = 8
tempu = 0.0"""

ap = network.WLAN (network.AP_IF) #Creates access point. 
#We create an instance of the class WLAN. The access point allows other clients to connect to the wifi
ap.active (True) #Activates network interface
ap.config (essid = 'bestNet20') #essid = wifi access point name
ap.config (authmode = 3, password = 'supersejtpass') #

pins = [machine.Pin(i, machine.Pin.OUT) for i in (16, 17, 21)] #we make the pins ready

#Reads temperature from SDA and SCL pins
"""def converter(data):
    value = (data[0] << 8) | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -=256.0
    return temp
"""
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

"""def updaterFunc(address, temp_reg, data):
    i2c.readfrom_mem_into(address, temp_reg, data)
    tempu = converter(data)
    print(tempu)
    if tempu < 25:      #Lights up green led if temperature is below 25 degrees
        pins[0].value(1)
        pins[1].value(0)
        pins[2].value(0)
    elif tempu < 28:    #Lights up yellow led if 25 <= temperature < 28 
        pins[0].value(0)
        pins[1].value(1)
        pins[2].value(0)
    else:
        pins[0].value(0)   #Lights up red led if temperature >= 28
        pins[1].value(0)
        pins[2].value(1)
    time.sleep(1)
"""

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