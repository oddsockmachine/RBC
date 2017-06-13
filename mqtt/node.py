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
        # schedule.clear() # TODO this will reset countdown to next run.
        # Need to only reschedule new jobs, remove deleted ones
        # print ([x.tags for x in schedule.jobs])
        # for j in self.jobs.all_jobs():
        #     schedule.every(j.period).seconds.do(j.func, "123", self.client).tag(j.name, 'temp', 'sensor')
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
        """Read in list of starting jobs from file on device. Run when node
        first starts up. Useful in case of power loss"""
        # self.jobs.add_job(Job("report_temp", 5, report_temp))
        # self.jobs.add_job(Job("report_humidity", 9, report_humidity))
        return

    def on_connect(self, client, userdata, flags, rc):
        """Subscribing in on_connect() means that if we lose the connection and
        reconnect then subscriptions will be renewed."""
        print("Node '{name}' connected with result code {rc}".format(name=self.name, rc=rc))
        print(userdata)

        action2cb = {"add": cb_add_job,
                    "del": cb_del_job,
                    "show": cb_show_jobs,
                    "report": cb_report_in,}
        for action, cb in action2cb.items():
            job_topic = "jobs/{}/{}/#".format(self.name, action)
            client.message_callback_add(job_topic, cb)
            client.subscribe(job_topic)  # Add, modify, remove, trigger, etc

def cb_report_in(client, userdata, msg):
    """Return internal stats to base station"""
    report = {}
    node = userdata
    report['name'] = node.name
    report['jobs'] = node.jobs.report_jobs()
    # print(report)
    client.publish("topic", dumps(report))
    return report


def cb_show_jobs(client, userdata, msg):
    print("cb_show_jobs")
    payload = loads(msg.payload)
    if payload.get("name"):
        return
    return

def cb_del_job(client, userdata, msg):
    print("Deleting job from "+userdata.name)
    attrs = vars(msg)
    print (', '.join("%s: %#s" % item for item in attrs.items()))

    return

def msg_fields_valid(payload):
    fields = "name period function pin".split(' ')
    missing_fields = [x for x in fields if x not in list(payload.keys())]
    if len(missing_fields)>0:
        print ("The following fields are missing: " + str(missing_fields))
        return False
    return True

def cb_add_job(client, userdata, msg):
    print("New job incoming...")
    payload = loads(msg.payload)
    if not msg_fields_valid(payload):
        return
    new_func = get_func(payload.get("function"))
    job_name = payload.get("name")
    pin = payload.get("pin", "no_pin")
    uid = job_name + pin  # Tag so we can identify this function later.
    # Must be hashable such that we can replace a job based on eg name/type/pin
    print("Adding job {} to {}".format(job_name, userdata.name))
    new_job = Job(job_name, int(payload.get("period")), new_func, payload)
    _self = userdata
    _self.jobs.add_job(new_job)
