# Code in MircoPython
# File name is main.py
# You will have to add mircopyhton to your Pico W.
# The best way to do this is though Thonny and there 
# are many videos showing how this can be done.

# Replace the SSID and PASSWORD with your own and wait for it to Connect


import network
import socket
import time
import machine  
from machine import Pin

in1 = Pin(2,Pin.OUT)
in2 = Pin(3,Pin.OUT)
in3 = Pin(4,Pin.OUT)
in4 = Pin(5,Pin.OUT)

pins = [in1,in2,in3,in4]
seqs = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
intled = machine.Pin("LED", machine.Pin.OUT)

desp = 1

def Motor():
    max = 0
    #print("Motor Running")
    while max < 1020:
        for step in seqs:
            max = max + 1
            for i in range(len(pins)):
                pins[i].value(step[i])
                time.sleep(0.001)
    pins[3].value(0)
     
    

#//------------------REPLACE-BELOW-------------------//#
ssid        =   '**************************************'
password    =   '**************************************'
#//------------------REPLACE-ABOVE-------------------//#




wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)


html = """<!DOCTYPE html>
    <html>
        <style>
            .textSize{
                font-size: 10vh;
            }
            .button {
              border: none;
              color: white;
              padding: 16px 32px;
              text-align: center;
              text-decoration: none;
              display: inline-block;
              font-size: 5vh;
              margin: 4px 2px;
              transition-duration: 0.4s;
              cursor: pointer;
            }

            .button1 {
              background-color: white; 
              color: black; 
              border: 2px solid #4CAF50;
            }

            .button1:hover {
              background-color: #4CAF50;
              color: white;
            }
            .button1: input checked + .button1{
                background-color: #4CAF50;
                color: white;
            }

            .button2 {
              background-color: white; 
              color: black; 
              border: 2px solid #E8300B;
            }

            .button2:hover {
              background-color: #E8300B;
              color: white;
            }
        </style>
        <head> <title>Pico W</title> </head>
        <center><body> <h1 class="textSize">Teddys Doggo Treats</h1>
            <p></p>
            <p>
            <form action="./dispense">
            <input class="button button1" type="submit" value="Dispense Treat"</>
            </form>
            </p>
            <p>
            <form action="./empty">
            <input class="button button2" type="submit" value="Reset"</>
            </form>
            </p>
            <br>
        </body></center>
    </html>
"""
 
# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
 
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
 
s = socket.socket()
s.bind(addr)
s.listen(1)
 
#print('listening on', addr)

stateis = ""
 
# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        #print('client connected from', addr)

        request = cl.recv(1024)
        #print(request)

        request = str(request)
        led_on = request.find('/dispense')
        led_off = request.find('/empty')
        ##print( 'led on = ' + str(led_on))
        ##print( 'led off = ' + str(led_off))

        if led_on == 6:
            #print("Treat Dispensed!!")
            intled.value(1)
            stateis = '<p class="textSize"> Treats Dispensed ' + str(desp) + "</p>"
            Motor()
            desp = desp + 1
            intled.value(0)
            

        if led_off == 6:
            #print("Empty")
            intled.value(0)
            stateis = '<p class="textSize">Next Bag</p>'
            desp = 1
     
        response = "<center>" + html + "" + stateis + "</center>"
        
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
 
    except OSError as e:
        cl.close()
        #print('connection closed')