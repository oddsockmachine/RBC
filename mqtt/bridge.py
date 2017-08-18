import paho.mqtt.client as mqtt
from channels import ChannelMgr
from pprint import pprint
import time
from json import dumps, loads
import socket
from conf import load_config


config = load_config()
name = 'bridge'
channel = ChannelMgr(name)
elk_port = 9400
elk_host = '192.168.55.34'
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((elk_host, elk_port))
# sock = s
client = mqtt.Client(client_id=name)

def send_to_elk(sock, data):
    sock.send(json.dumps(data))
    sock.send('\n')


def sensor_cb(client, userdata, msg):
    mid = msg.mid
    payload = loads(msg.payload.decode("utf-8"))
    timestamp = msg.timestamp
    url = msg.topic
    print(url, payload['value'])
    # send_to_elk(sock, payload)

def log_cb(client, userdata, msg):
    mid = msg.mid
    payload = loads(msg.payload.decode("utf-8"))
    timestamp = msg.timestamp
    url = msg.topic
    print(url, payload)
    # send_to_elk(sock, payload)

def error_cb(client, userdata, msg):
    mid = msg.mid
    payload = loads(msg.payload.decode("utf-8"))
    timestamp = msg.timestamp
    url = msg.topic
    print(url, payload)
    # send_to_elk(sock, payload)

# def on_connect(self, client, userdata, flags, rc):
#     client.message_callback_add("#", show_all)
#     client.subscribe("#")  # Add, modify, remove, trigger, etc

# client.on_connect = on_connect

def presence_msg(connected=True):
    return dumps({'presence': 'Connected' if connected else 'Disconnected', 'node': name})
# LastWill must be set before connect()
presence_channel = channel.presence()
client.will_set(presence_channel, presence_msg(False), 0, False)


client.connect(config['MQTT_URL'], config['MQTT_PORT'], config['MQTT_KEEPALIVE'])
client.message_callback_add("sensors/#", sensor_cb)
client.message_callback_add("logs/#", log_cb)
client.message_callback_add("errors/#", error_cb)
client.subscribe("sensors/#")  # Add, modify, remove, trigger, etc
client.subscribe("logs/#")  # Add, modify, remove, trigger, etc
client.subscribe("errors/#")  # Add, modify, remove, trigger, etc

client.loop_start()
client.publish(presence_channel, presence_msg(True))

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        client.disconnect()
        break
exit(0)
