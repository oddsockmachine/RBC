https://home-assistant.io/blog/2016/08/31/esp8266-and-micropython-part2/


https://www.hackster.io/bucknalla/mqtt-micropython-044e77

import ubinascii
import machine
from umqtt2 import MQTTClient

CONFIG = {
    "broker": "192.168.0.12",
    "sensor_pin": 0,
    "client_id": b"esp8266_" + ubinascii.hexlify(machine.unique_id()),
    "topic": b"topic",
}

client = MQTTClient(CONFIG['client_id'], CONFIG['broker'])
client.connect()

data = "foo"
client.publish('{}/{}'.format(CONFIG['topic'], CONFIG['client_id']), bytes(str(data), 'utf-8'))
client.publish('topic', bytes(str(data), 'utf-8'))



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

from time import sleep
def send_measurements(delay, log):
    vcc = machine.ADC(1)
    while True:
        t, h = measure(d, 3, log)
        batt = vcc.read()
        data = "{}c, {}%, {}vcc".format(t,h,batt)
        client.publish('{}/{}'.format(CONFIG['topic'], CONFIG['client_id']), bytes(str(data), 'utf-8'))
        sleep(delay)
