import paho.mqtt.client as mqtt
from channels import ChannelMgr
from pprint import pprint
import time
from json import dumps, loads
import socket
from conf import load_config

def send_to_elk(client, userdata, msg):
    mid = msg.mid
    payload = loads(msg.payload.decode("utf-8"))
    timestamp = msg.timestamp
    url = msg.topic
    print("ELK:\t", url, payload)
    def send_to_elk(sock, data):
        sock.send(json.dumps(data))
        sock.send('\n')
    return

def send_to_db(client, userdata, msg):
    mid = msg.mid
    payload = loads(msg.payload.decode("utf-8"))
    timestamp = msg.timestamp
    url = msg.topic
    # print("DB:\t", url, payload)
    topic, node_name = url.split('/')
    print(node_name, topic)
    if topic == 'presence':
        print("{}.presence = {}".format(node_name, payload.get('presence')))
    elif topic == 'report':
        print("{} = {}".format(node_name, payload))
    return


def send_to_file(client, userdata, msg):
    mid = msg.mid
    payload = loads(msg.payload.decode("utf-8"))
    timestamp = msg.timestamp
    url = msg.topic
    time = payload['timestamp'].split('.')[0]
    values = loads(payload['value'].replace("'", '"'))
    # temp = values['temp']
    log_line = '{}, {}\n'.format(time, values)
    with open('logfile.txt', 'a') as logfile:
        logfile.write(log_line)
    return



router = {
    'elk': send_to_elk,
    'db': send_to_db,
    'file': send_to_file,
}

routes = {
    'presence': ['elk', 'db'],
    'sensors': ['elk'],#, 'file'],
    'logs': ['elk'],
    'errors': ['elk'],
    'report': ['elk', 'db'],
}

def msg_cb(client, userdata, msg):
    topic = msg.topic.split("/")[0]
    for route in routes.get(topic):
        # try:
        r_func = router.get(route)
        r_func(client, userdata, msg)
        # except:
        #     print("Topic {} not recognized".format(topic))
        #     pass

config = load_config()
name = 'bridge'
channel = ChannelMgr(name)
elk_port = 9300
elk_host = '192.168.0.15'
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((elk_host, elk_port))
# sock = s
client = mqtt.Client(client_id=name)

def presence_msg(connected=True):
    return dumps({'presence': 'Connected' if connected else 'Disconnected', 'node': name})

client.will_set(channel.presence(), presence_msg(False), 0, False)
client.connect(config['MQTT_URL'], config['MQTT_PORT'], config['MQTT_KEEPALIVE'])

for topic in config['topics']:
    channel_name = topic + '/#'
    client.message_callback_add(channel_name, msg_cb)
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
