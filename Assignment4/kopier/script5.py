import machine, neopixel
import network
import socket
import time

#Setup initial values and create instance of the machine, i2c, and the neopixel
data = bytearray(2)
input1 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
i2c = machine.I2C(scl=machine.Pin(22),sda=machine.Pin(23))
np = neopixel.NeoPixel(machine.Pin(27),2)
address = 24
temp_reg = 5
res_reg = 8
tempu = 0.0

#converts the temperature 
def converter(data):
    value = (data[0] << 8) | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -=256.0
    return temp

#Setup network parameters
ap = network.WLAN (network.AP_IF)
ap.active (True)
ap.config (essid = 'bestNet20')
ap.config (authmode = 3, password = 'password')

#initiate pins for the LEDs
pins = [machine.Pin(i, machine.Pin.OUT) for i in (16, 17, 21)]

#main HTML message
html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 Pins</title> </head>
    <body> <h1>ESP32 Pins</h1>
        <table border="1"> <tr><th>Variable</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""
#create socket connection
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    #read the inputs from the button and temperture
    #The temperature will no longer control the LEDs
    button = input1.value()
    i2c.readfrom_mem_into(address, temp_reg, data)
    tempu = converter(data)
    print(tempu)

    #adding the desired values to dictionaries for accesability when called from the server
    pinDict = {"16":pins[0].value(), "17":pins[1].value(), "18":pins[2].value()}
    buttonDict = {"button":button}
    tempDict = {"Temperature":tempu}
    resources = [pinDict, buttonDict, tempDict]

    #wait for incomming connection
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        #The line will be the messages recived from whoever connects
        #The line is compared to some requirements, this how the right responce for each message recived gets sendt
        line = cl_file.readline()
        print(line)
        if line == b'GET / resources\r\n':
            response = "\{Pin 16\:%d, Pin 17\:%d, Pin 18\:%d, Button\:%d, Temperature\:%f\}" % (pins[0].value(), pins[1].value(), pins[2].value(), button, tempu)
            cl.send(response)
            cl.close()
            break
        elif line == b'GET / resources/pins\r\n':
            response = "\{Pin 16\:%d, Pin 17\:%d, Pin 18\:%d\}" % (pins[0].value(), pins[1].value(), pins[2].value())
            cl.send(response) #send the responce and close the connection
            cl.close()
            break
        elif line == b'GET / resources/pins/16\r\n':
            response = "\{Pin 16\:%d\}" % pins[0].value()
            cl.send(response)
            cl.close()
            break
        elif line == b'GET / resources/pins/17\r\n':
            response = "\{Pin 17\:%d\}" % pins[1].value()
            cl.send(response)
            cl.close()
            break
        elif line == b'GET / resources/pins/18\r\n':
            response = "\{Pin 18\:%d\}" % pins[2].value()
            cl.send(response)
            cl.close()
            break
        elif line == b'GET / resources/temp\r\n':
            response = "\{Temperature\:%f\}" % tempu
            cl.send(response)
            cl.close()
            break
        elif line == b'GET / resources/button\r\n':
            response = "\{Button\:%d\}" % button
            cl.send(response)
            cl.close()
            break
        elif line == b'PATCH / LED/green/on\r\n':
            pins[0].value(1) #turn on or off the different LEDs
            cl.close()
            break
        elif line == b'PATCH / LED/green/off\r\n':
            pins[0].value(0)
            cl.close()
            break
        elif line == b'PATCH / LED/yellow/on\r\n':
            pins[1].value(1)
            cl.close()
            break
        elif line == b'PATCH / LED/yellow/off\r\n':
            pins[1].value(0)
            cl.close()
            break
        elif line == b'PATCH / LED/red/on\r\n':
            pins[2].value(1)
            cl.close()
            break
        elif line == b'PATCH / LED/red/off\r\n':
            pins[2].value(0)
            cl.close()
            break
        elif line == b'PATCH / LED/all/on\r\n':
            pins[0].value(1)
            pins[1].value(1)
            pins[2].value(1)
            cl.close()
            break
        elif line == b'PATCH / LED/all/off\r\n':
            pins[0].value(0)
            pins[1].value(0)
            pins[2].value(0)
            cl.close()
            break
        elif "NEO" in str(line):
            #The message recieved will be on our specified form
            #from this form can integers be extracted
            #these then form the basis of the neopixel colour
            rgb = [int(str(line)[14:17]), int(str(line)[17:20]), int(str(line)[20:23])]
            print(rgb)
            np[0] = (rgb[0],rgb[1],rgb[2])
            np[1] = (rgb[0],rgb[1],rgb[2])
            np.write()
            cl.close()
            break

        if not line or line == b'\r\n':
            #the rows get added to a single string, that can be send and used by the webpage
            rows1 = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
            rows2 = ['<tr><td>%s</td><td>%f</td></tr>' % ("Temperature", tempu)]
            rows3 = ['<tr><td>%s</td><td>%d</td></tr>' % ("Button state", button)]
            rows = rows1 + rows2 + rows3
            response = html % '\n'.join(rows)
            cl.send(response)
            cl.close()
            break
    
