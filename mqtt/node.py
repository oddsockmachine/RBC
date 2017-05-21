import paho.mqtt.client as mqtt
from jobs import JobList, Job
from functions import *
import schedule
from functools import partial
from json import loads

class Node(object):
    """docstring for Node."""
    def __init__(self, name):
        super(Node, self).__init__()
        self.name = name
        self.client = mqtt.Client(client_id="name")
        self.client.user_data_set(self)
        self.client.on_connect = self.on_connect
        self.jobs = JobList(self.client)
        self.init_pin_mappings()
        self.load_in_jobs()
        # self.load_subscriptions()
        # for j in self.jobs.all_jobs():
        #     schedule.every(j.period).seconds.do(j.func, "123", self.client).tag(j.name, 'temp', 'sensor')
        return

    def refresh_schedule(self):
        for j in self.jobs.all_jobs():
            schedule.every(j.period).seconds.do(j.func, "123", self.client).tag(j.name, 'temp', 'sensor')
        return

    def init_pin_mappings(self):
        self.pin_mappings = {}
        return

    def start(self):
        self.client.connect("127.0.0.1", 1883, 60)
        self.client.loop_start()
        return

    def disconnect(self):
        self.client.disconnect()


    def get_all_jobs(self):
        return schedule.jobs

    def load_in_jobs(self):
        # self.jobs.add_job(Job("report_temp", 5, report_temp))
        # self.jobs.add_job(Job("report_humidity", 9, report_humidity))
        return

    def load_callbacks(self):
        return

    def on_connect(self, client, userdata, flags, rc):
        print("Node '{name}' connected with result code {rc}".format(name=self.name, rc=rc))
        print(userdata)
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        job_topic = "jobs/#"
        add_topic = "jobs/{}/add/#".format(self.name)
        del_topic = "jobs/{}/del/#".format(self.name)

        # print(job_topic)
        # client.message_callback_add("actuator/#", cb_all_actuator)
        # client.subscribe("actuator/#")
        client.message_callback_add(job_topic, cb_all_jobs)
        client.message_callback_add("jobs/{}/add/#".format(self.name), cb_add_job)
        client.message_callback_add("jobs/{}/del/#".format(self.name), cb_del_job)
        client.subscribe(job_topic)  # Add, modify, remove, trigger, etc
        client.subscribe("jobs/{}/del/#")  # Add, modify, remove, trigger, etc
        client.subscribe("jobs/{}/add/#")  # Add, modify, remove, trigger, etc



def cb_all_actuator(client, userdata, msg):
    print("cb_all_actuator!!!!!!!!!!!!!!!!!")
    print(msg.payload)

def cb_all_jobs(client, userdata, msg):
    print("cb_all_jobs")

def cb_del_job(client, userdata, msg):
    print("Deleting job from "+userdata.name)
    return


def cb_add_job(client, userdata, msg):
    print("Adding job to " + userdata.name)
    print(msg.payload)
    payload = loads(msg.payload)
    new_func = get_func(payload.get("function"))
    print(payload['name'])
    print ("!!!")
    _self = userdata
    _self.jobs.add_job(Job(payload.get("name"), 7, new_func))
    _self.refresh_schedule()
    attrs = vars(msg)
    print (', '.join("%s: %s" % item for item in attrs.items()))
    print(userdata.name)
    print(userdata.get_all_jobs())
    print(client)
    print(msg)
