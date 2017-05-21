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
        """Empty the node's schedule, rebuild from its internal list of jobs"""
        schedule.clear() # TODO this will reset countdown to next run.
        # Need to only reschedule new jobs, remove deleted ones
        # print ([x.tags for x in schedule.jobs])
        for j in self.jobs.all_jobs():
            schedule.every(j.period).seconds.do(j.func, "123", self.client).tag(j.name, 'temp', 'sensor')
        return

    def init_pin_mappings(self):
        # Handle how pins and jobs interact, ensure no conflicts
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

        action2cb = {"add": cb_add_job,
                    "del": cb_del_job,
                    "show": cb_show_jobs,}
        for action, cb in action2cb.items():
            job_topic = "jobs/{}/{}/#".format(self.name, action)
            client.message_callback_add(job_topic, cb)
            client.subscribe(job_topic)  # Add, modify, remove, trigger, etc

        # job_topic = "jobs/{}/show/#".format(self.name)
        # add_topic = "jobs/{}/add/#".format(self.name)
        # del_topic = "jobs/{}/del/#".format(self.name)        #
        # client.message_callback_add(job_topic, cb_show_jobs)
        # client.message_callback_add("jobs/{}/add/#".format(self.name), cb_add_job)
        # client.message_callback_add("jobs/{}/del/#".format(self.name), cb_del_job)
        # client.subscribe(job_topic)  # Add, modify, remove, trigger, etc
        # client.subscribe("jobs/{}/del/#")  # Add, modify, remove, trigger, etc
        # client.subscribe("jobs/{}/add/#")  # Add, modify, remove, trigger, etc



def cb_all_actuator(client, userdata, msg):
    print("cb_all_actuator!!!!!!!!!!!!!!!!!")
    print(msg.payload)

def cb_show_jobs(client, userdata, msg):
    print("cb_show_jobs")
    payload = loads(msg.payload)
    if payload.get("name"):
        return
    return

def cb_del_job(client, userdata, msg):
    print("Deleting job from "+userdata.name)
    return

def validate_msg_fields():
    return

def cb_add_job(client, userdata, msg):
    print("Adding job to " + userdata.name)
    fields = "name period function".split(' ')
    payload = loads(msg.payload)
    missing_fields = [x for x in fields if x not in list(payload.keys())]
    if len(missing_fields)>0:
        print ("The following fields are missing:")
        print (missing_fields)
        return
    # print(msg.payload)
    new_func = get_func(payload.get("function"))
    print(payload['name'])
    name = payload.get("name")
    pin = payload.get("pin", "no_pin")
    uid = name + pin  # Tag so we can identify this function later.
    # Must be hashable such that we can replace a job based on eg name/type/pin
    new_job = Job(name, int(payload.get("period")), new_func)
    # new_job.tags = "name="+name
    _self = userdata
    _self.jobs.add_job(new_job)
    _self.refresh_schedule()
    # attrs = vars(msg)
    # print (', '.join("%s: %#s" % item for item in attrs.items()))
    # print(userdata.name)
    # print(userdata.get_all_jobs())
    # print(client)
    # print(msg)
