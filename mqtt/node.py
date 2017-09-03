import paho.mqtt.client as mqtt
from sys import argv
from jobs import *
from sensors import *
from sensor_set import SensorSet
import schedule
import time
from json import loads, dumps
from logger import log_catch
from collections import deque
from conf import load_config
from channels import ChannelMgr


class Node(object):
    """docstring for Node."""
    def __init__(self, name):
        super(Node, self).__init__()
        self.config = load_config()  # Load config from default path
        self.name = name
        self.client = mqtt.Client(client_id=name)
        self.client.user_data_set(self)
        self.client.on_connect = self.on_connect
        self.jobs = JobList(self.client)
        self.load_in_jobs()
        self.sensor_set = SensorSet()
        self.error_log = deque([], self.config['err_log_size'])
        self.logs = deque([], self.config['log_size'])
        self.channel = ChannelMgr(name)
        # self.load_subscriptions()
        return

    def log(self, msg):
        # log will auto-rotate if past max len
        if self.config['debug']:
            print(msg)
        msg_data = dumps({'timestamp': str(datetime.now()), 'log': str(msg), 'node': self.name})
        self.logs.append(msg_data)

    def refresh_schedule(self):
        """Empty the node's schedule, rebuild from its internal list of jobs"""
        # schedule.clear() # TODO this will reset countdown to next run.
        # Need to only reschedule new jobs, remove deleted ones
        # print ([x.tags for x in schedule.jobs])
        # for j in self.jobs.all_jobs():
        #     schedule.every(j.period).seconds.do(j.func, "123", self.client).tag(j.name, 'temp', 'sensor')
        return

    def start(self):
        def presence_msg(connected=True):
            return dumps({'presence': 'Connected' if connected else 'Disconnected', 'node': self.name})
        # LastWill must be set before connect()
        presence_channel = self.channel.presence()
        self.client.will_set(presence_channel, presence_msg(False), 0, False)
        self.client.connect(self.config['MQTT_URL'], self.config['MQTT_PORT'], self.config['MQTT_KEEPALIVE'])
        self.client.loop_start()
        self.client.publish(presence_channel, presence_msg(True))
        return

    def disconnect(self):
        """Disconnects safely, sends LWT msg"""
        print("Safely disconnecting")
        self.client.disconnect()

    def get_all_jobs(self):
        return schedule.jobs

    def load_in_jobs(self):
        """Read in list of starting jobs from file on device. Run when node
        first starts up. Useful in case of power loss"""
        if self.config['schedule']['error_reporting']['enable']:
            error_reporter = InternalJob(self.config['schedule']['error_reporting']['period'], self, "error_reporter", self.report_errors)
            self.jobs.add_job(error_reporter)
        if self.config['schedule']['log_reporting']['enable']:
            log_reporter = InternalJob(self.config['schedule']['log_reporting']['period'], self, "log_reporter", self.report_logs)
            self.jobs.add_job(log_reporter)
        return

    def backup_to_disk(self):
        """Save state of all jobs and sensors to file on device. Run when
        changes are made, so state can be restored with load_in_jobs"""
        return

    def log_error(self, msg):
        """Send an error message to this node's error log
        Typically called by the log_catch contextmanager"""
        self.error_log.append(msg)

    def report_errors(self):
        """If there are errors in the logs, compile them all and publish.
        Clear the log after"""
        if len(self.error_log) == 0: # Ignore if no error msgs
            return
        error_channel = self.channel.errors()
        error_msgs = ",,,".join(self.error_log)  # convert list of json messages into str
        self.client.publish(error_channel, dumps(list(self.error_log)))  # Publish
        self.error_log = []  # Clear error log, to avoid repeats

    def report_logs(self):
        """If there are logs in the logs, compile them all and publish.
        Clear the log after"""
        if len(self.logs) == 0: # Ignore if no log msgs
            return
        log_channel = self.channel.logs()
        log_msgs = ",,,".join(self.logs)  # convert list of json messages into str
        self.client.publish(log_channel, dumps(list(self.logs)))  # Publish
        self.logs = deque([], 50)

    def on_connect(self, client, userdata, flags, rc):
        """Subscribing in on_connect() means that if we lose the connection and
        reconnect then subscriptions will be renewed."""
        print("Node '{name}' connected with result code {rc}".format(name=self.name, rc=rc))
        action2cb = {"add": cb_add_job,
                    "del": cb_del_job,
                    # "show": cb_show_jobs,
                    "trigger": cb_trigger_job,
                    "get_logs": cb_report_logs,
                    "query_sensor": cb_query_sensor,
                    # "get_errors": cb_show_errors,
                    "report": cb_report_in,}
        for action, cb in action2cb.items():
            job_topic = "jobs/{}/{}/#".format(self.name, action)
            job_topic = self.channel.jobs(action)
            client.message_callback_add(job_topic, cb)
            client.subscribe(job_topic)  # Add, modify, remove, trigger, etc


def cb_report_in(client, userdata, msg):
    """Return internal stats to base station"""
    _self = userdata
    _self.log("Reporting in")
    report = {}
    report['name'] = _self.name
    report['jobs'] = _self.jobs.all_jobs()
    report['sensor_set'] = _self.sensor_set.report()
    client.publish(_self.channel.report(), dumps(report))
    return report


def cb_report_logs(client, userdata, msg):
    """Return internal stats to base station"""
    _self = userdata
    _self.log("Sending logs")
    report = {}
    report['name'] = _self.name
    report['logs'] = _self.report_logs()
    client.publish(_self.channel.logs(), dumps(report))
    return report

def cb_show_jobs(client, userdata, msg):
    self.log("cb_show_jobs")
    payload = loads(msg.payload.decode())
    if payload.get("name"):
        return  # TODO
    return

def cb_query_sensor(client, userdata, msg):
    _self = userdata
    _self.log("cb_query_sensor")
    payload = loads(msg.payload.decode())
    with log_catch(_self):
        sensor_uid = payload["sensor_uid"]
        print(sensor_uid)
        _self.log("querying {}".format(sensor_uid))
        sensor = _self.sensor_set.get_sensor_by_id(sensor_uid)
        reading = sensor.read()
        print(reading)
        # TODO publish results
    return

def cb_trigger_job(client, userdata, msg):
    print("cb_trigger_job")
    payload = loads(msg.payload.decode())
    if payload.get("name"):
        return  # TODO
    return

def cb_del_job(client, userdata, msg):
    self.log("Deleting job from "+userdata.name)
    attrs = vars(msg)
    print(', '.join("%s: %#s" % item for item in attrs.items()))
    return

def validate_msg_fields_valid(payload):
    fields = "name period sensor_type pin".split(' ')
    missing_fields = [x for x in fields if x not in list(payload.keys())]
    if len(missing_fields)>0:
        raise Exception("The following fields are missing: " + str(missing_fields))
    return True

def cb_add_job(client, userdata, msg):
    _self = userdata
    _self.log("New job incoming...")
    payload = loads(msg.payload.decode())
    with log_catch(_self):
        # validate_msg_fields_valid(payload)
        sensor_type = payload["sensor_type"]
        sensor_class = get_sensor_class(sensor_type)
        job_name = payload["name"]
        pin = payload["pin"]
        period = int(payload["period"])
        uid = "~".join([_self.name, sensor_type, job_name, pin])  # Tag so we can identify this function later.
        # Must be hashable such that we can replace a job based on eg name/type/pin
        _self.log("Adding job {} type {}".format(job_name, sensor_class.__name__))
    # with log_catch(_self):
        new_sensor = sensor_class(uid, pin, job_name)
        _self.sensor_set.add_sensor(new_sensor)
        new_job = SensorJob(period, _self, new_sensor)
        _self.jobs.add_job(new_job)


if __name__ == '__main__':
    try:
        node_name = argv[1]
    except:
        print("Please provide config file")
        exit(1)
    myNode = Node(node_name)
    myNode.start()
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            myNode.disconnect()
            break
    exit(0)
