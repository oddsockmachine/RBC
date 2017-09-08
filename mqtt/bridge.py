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
elk_port = 9300
elk_host = '192.168.0.15'
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((elk_host, elk_port))
# sock = s
client = mqtt.Client(client_id=name)

def send_to_elk(sock, data):
    sock.send(json.dumps(data))
    sock.send('\n')

def presence_cb(client, userdata, msg):
    mid = msg.mid
    payload = loads(msg.payload.decode("utf-8"))
    timestamp = msg.timestamp
    url = msg.topic
    print(url, payload)
    # send_to_elk(sock, payload)

def sensors_cb(client, userdata, msg):
    mid = msg.mid
    payload = loads(msg.payload.decode("utf-8"))
    timestamp = msg.timestamp
    url = msg.topic
    print(url, payload['value'])
    # send_to_elk(sock, payload)

def logs_cb(client, userdata, msg):
    mid = msg.mid
    payload = loads(msg.payload.decode("utf-8"))
    timestamp = msg.timestamp
    url = msg.topic
    print(url, payload)
    # send_to_elk(sock, payload)

def errors_cb(client, userdata, msg):
    mid = msg.mid
    payload = loads(msg.payload.decode("utf-8"))
    timestamp = msg.timestamp
    url = msg.topic
    print(url, payload)
    # send_to_elk(sock, payload)

def report_cb(client, userdata, msg):
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
client.will_set(channel.presence(), presence_msg(False), 0, False)

client.connect(config['MQTT_URL'], config['MQTT_PORT'], config['MQTT_KEEPALIVE'])

# Hideous hack to find all user-defined callback functions
cb_funcs = {x:y for x,y in globals().items() if str(x).endswith("_cb")}
topics = ['sensors', 'logs', 'errors', 'presence', 'report']
for topic in topics:
    cb_name = topic + '_cb'
    cb_func = cb_funcs[cb_name]
    channel_name = topic + '/#'
    client.message_callback_add(channel_name, cb_func)
    client.subscribe(channel_name)  # Add, modify, remove, trigger, etc

client.loop_start()
client.publish(channel.presence(), presence_msg(True))

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        client.disconnect()
        break
exit(0)
