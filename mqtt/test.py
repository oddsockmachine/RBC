import paho.mqtt.client as mqtt
import time
import schedule
from jobs import get_all_jobs, JobList

total = 0

def update_schedule(jobs, new_info):

    return

def cb_all_actuator(client, userdata, msg):
    print("cb_all_actuator")
    print(msg.payload)
def cb_irrigation_actuator(client, userdata, msg):
    print("cb_irrigation_actuator")
    print(msg.payload)
def cb_ventilation_actuator(client, userdata, msg):
    print("cb_ventilation_actuator")
    print(msg.payload)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("topic/thing/")
    client.subscribe("actuator/#")
    client.message_callback_add("actuator/#", cb_all_actuator)
    client.message_callback_add("actuator/temp", cb_irrigation_actuator)
    client.message_callback_add("actuator/hmdy", cb_ventilation_actuator)



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    global total
    total += 1

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)

client.loop_start()
# client.loop_forever()

joblist = JobList(client)

for j in get_all_jobs():
    schedule.every(j.period).seconds.do(j.func, "123").tag(j.name,'temp', 'sensor')

# schedule.every(5).seconds.do(report_temp, "123").tag('temp', 'sensor')
while True:
    schedule.run_pending()
    time.sleep(1)
