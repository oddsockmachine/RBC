# https://home-assistant.io/blog/2016/08/31/esp8266-and-micropython-part2/
# https://www.hackster.io/bucknalla/mqtt-micropython-044e77

import ubinascii
import machine
from umqtt2 import MQTTClient
import dht
from time import sleep


sensors = {"ID": sensor_obj(pin, type, etc)}


CONFIG = {
    "broker": "192.168.0.12",
    "sensor_pin": 0,
    "client_id": "esp8266_" + str(ubinascii.hexlify(machine.unique_id())),
    "topic": "topic",
}

client = MQTTClient(CONFIG['client_id'], CONFIG['broker'])

def connect():
    ## TODO Auto-connect, retry-backoff, and catch errors
    client.connect()

def disconnect():
    client.disconnect()


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


def send_measurements(delay, log):
    d = dht.DHT11(machine.Pin(5))
    vcc = machine.ADC(1)
    ## TODO Add some try-catch to detect broken connection
    while True:
        t, h = measure(d, 3, log)
        batt = vcc.read()
        data = "{}c, {}%, {}vcc".format(t,h,batt)
        client.publish('{}/{}'.format(CONFIG['topic'], CONFIG['client_id']), bytes(str(data), 'utf-8'))
        sleep(delay)
    return
