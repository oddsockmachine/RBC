import paho.mqtt.client as mqtt
from jobs import JobList, Job
from sensors import *
from functions import *
import schedule
import time
from json import loads, dumps
from logger import log_catch


class Node(object):
    """docstring for Node."""
    def __init__(self, name):
        super(Node, self).__init__()
        self.name = name
        self.client = mqtt.Client(client_id=name)
        self.client.user_data_set(self)
        self.client.on_connect = self.on_connect
        self.jobs = JobList(self.client)
        self.init_pin_mappings()
        self.load_in_jobs()
        self.sensor_set = SensorSet()
        self.error_log = []
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
        def presence_msg(connected=True):
            return dumps({'presence': 'Connected' if connected else 'Disconnected', 'node': self.name})
        # LassWill must be set before connect()
        presence_channel = 'presence/{}'.format(self.name)
        self.client.will_set(presence_channel, presence_msg(False), 0, False)

        # self.client.connect("192.168.0.15", 1883, 60)
        self.client.connect("127.0.0.1", 1883, 60)
        self.client.loop_start()
        self.client.publish(presence_channel, presence_msg(True))
        return

    def disconnect(self):
        print("Safely disconnecting")
        self.client.disconnect()

    def get_all_jobs(self):
        return schedule.jobs

    def load_in_jobs(self):
        """Read in list of starting jobs from file on device. Run when node
        first starts up. Useful in case of power loss"""
        error_reporter = Job("error_reporter", 5, self.report_errors, {'pin':''})
        self.jobs.add_job(error_reporter)

        return

    def log_error(self, msg):
        self.error_log.append(msg)

    def report_errors(self, a, b):
        print("Publishing error report")
        error_channel = 'errors/{}'.format(self.name)
        error_msgs = ",,,".join(self.error_log)  # convert list of json messages into str
        self.client.publish(error_channel, error_msgs)  # Publish
        self.error_log = []  # Clear error log, to avoid repeats

    def on_connect(self, client, userdata, flags, rc):
        """Subscribing in on_connect() means that if we lose the connection and
        reconnect then subscriptions will be renewed."""
        print("Node '{name}' connected with result code {rc}".format(name=self.name, rc=rc))
        print(userdata)

        action2cb = {"add": cb_add_job,
                    "del": cb_del_job,
                    "show": cb_show_jobs,
                    # "get_errors": cb_show_errors,
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
    report['jobs'] = [dictj.__dict__ for j in node.jobs.all_jobs()]
    print(report)
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
    with log_catch(_self):
        new_sensor = Mock_Sensor(uid, pin, job_name)
        _self.sensor_set.add_sensor(new_sensor)

    _self.jobs.add_job(new_job)


if __name__ == '__main__':
    print("Please provide config file")
    myNode = Node("bar")
    myNode.start()
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            myNode.disconnect()
            break
    exit(0)
