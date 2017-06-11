import paho.mqtt.client as mqtt
import time
import schedule
from node import Node


myNode = Node("foo")
myNode.start()
while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except KeyboardInterrupt:
        myNode.disconnect()
        break
exit(0)
