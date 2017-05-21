import paho.mqtt.client as mqtt
import time
import schedule
from node import Node



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
    # client.subscribe("topic/thing/")
    # client.subscribe("actuator/#")
    # client.message_callback_add("actuator/#", cb_all_actuator)
    # client.message_callback_add("actuator/temp", cb_irrigation_actuator)
    # client.message_callback_add("actuator/hmdy", cb_ventilation_actuator)



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)

client.loop_start()
# client.loop_forever()

testNode = Node("foo")
testNode.start()
while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except KeyboardInterrupt:
        testNode.disconnect()
        exit(0)
