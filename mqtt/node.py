import paho.mqtt.client as mqtt
from jobs import JobList, Job
from functions import *
import schedule
from functools import partial


class Node(object):
    """docstring for Node."""
    def __init__(self, name):
        super(Node, self).__init__()
        self.name = name
        self.client = mqtt.Client(client_id="name")
        self.client.user_data_set(self)
        self.client.on_connect = self.on_connect
        self.jobs = JobList(self.client)
        # js = [report_temp, report_humidity]
        # jx =
        self.cb_all_jobs = partial(cb_all_jobs)
        self.init_pin_mappings()
        self.load_in_jobs()
        # self.load_subscriptions()
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
        self.jobs.add_job(Job("report_temp", 5, report_temp))
        self.jobs.add_job(Job("report_humidity", 9, report_humidity))
        return

    def load_callbacks(self):
        return

    # def load_subscriptions(self):
    #     job_topic = "jobs/{}/#".format(self.name)
    #     print(job_topic)
    #     self.client.message_callback_add("actuator/#", cb_all_actuator)
    #     self.client.message_callback_add(job_topic, cb_all_jobs)
    #     self.client.subscribe("actuator/#")
    #     self.client.subscribe(job_topic)  # Add, modify, remove, trigger, etc

        return

    def on_connect(self, client, userdata, flags, rc):
        print("Node '{name}' connected with result code {rc}".format(name=self.name, rc=rc))
        print(userdata)
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        job_topic = "jobs/#"
        print(job_topic)
        client.message_callback_add("actuator/#", cb_all_actuator)
        client.message_callback_add(job_topic, cb_all_jobs)
        client.subscribe("actuator/#")
        client.subscribe(job_topic)  # Add, modify, remove, trigger, etc



    # def create_job_cb(self):
    #     _self = self
    #     def cb_all_jobs(client=client, userdata=userdata, msg=msg):
    #         print("cb_all_jobs")
    #         print(_self.name)
    #         print(msg.payload)
    #         print(userdata)
    #         print(client)
    #         print(msg)
    #     return cb_all_jobs

def cb_all_actuator(client, userdata, msg):
    print("cb_all_actuator!!!!!!!!!!!!!!!!!")
    print(msg.payload)

def cb_all_jobs(client, userdata, msg):
    print("cb_all_jobs")
    print(msg.payload)
    print(userdata.name)
    print(userdata.get_all_jobs())
    print(client)
    print(msg)
