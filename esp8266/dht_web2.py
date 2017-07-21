import machine
import dht
d = dht.DHT11(machine.Pin(5))

def measure(_d, readings, log):
    h = []
    t = []
    for i in range(readings):
        _d.measure()
        t.append(_d.temperature())
        h.append(_d.humidity())
    temp = int(sum(t)/len(t))
    hum = int(sum(h)/len(h))
    if  log:
        print("{}c, {}%".format(temp,hum))
    return temp, hum

measure(d, 3, True)

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>Temperature + Humidity</h1>
        <h2>%s</h2>
    </body>
</html>
"""

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)




while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    t, h = measure(d, 3, True)
    data = "{}c, {}%".format(t,h,True)
    response = html % data
    cl.send(response)
    cl.close()
