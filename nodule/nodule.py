import paho.mqtt.client as mqtt
from jobs import *
from components.sensors import *
from components.gpio_set import *
import schedule
import time
import requests
from json import loads, dumps
from logger import log_catch
from reporter import Reporter
from collections import deque
from configurator import load_config_from_disk, write_config_to_disk, CONFIG, get_uid
from channels import ChannelMgr


class Nodule(object):
    """docstring for Nodule."""
    def __init__(self):
        super(Nodule, self).__init__()
        self.config = CONFIG  # Take config from disk - first attempt, only need basics
        self.UID = get_uid()  # UID identifies this node on the manager and logger
        self.client = mqtt.Client(client_id=self.UID)
        self.channel_mgr = ChannelMgr(self.UID)  # ChannelMgr provides easy access to channel URLs
        self.reporter = Reporter(self)  # Reporter manages sending reports/readings over mqtt, or buffering in case of connectivity issues
        self.publish = self.reporter.publish  # Easy-access reporting functions delegate to reporter
        self.debug = self.reporter.debug
        self.log_error = self.reporter.log_error
        self.start_mqtt()  # Connect to the Mosquitto broker - used to send readings/reports, receive triggers from manager
        # TODO update internal time if hw==espx
        self.fetch_remote_config()  # We've just woken, so try to refresh config from source of truth
        self.config = load_config_from_disk()  # Load config from disk now that jobs, components etc are up-to-date
        self.gpio_set = GPIO_Set(self)  # Set up sensors/actuators/external components according to config
        self.jobs = JobList(self)  # Set up jobs/schedules according to config
        self.wake_time = datetime.now()  # We will sometimes report this/track uptime
        return

    def fetch_remote_config(self):
        """Try to load in config from central manager.
        Config will already have been read from disk, but it may have been
        updated since last read/restart.
        If this fails due to connectivity, just fall back to disk config."""
        mgr_conf = self.config['hardware']['manager']
        endpoints = mgr_conf['get_config_endpoints']
        for cfg_type, endpoint in endpoints.items():
            config_url = 'http://{url}:{port}/{endpoint}'.format(url=mgr_conf['url'],port=mgr_conf['port'],endpoint=endpoint).format(n_id=self.UID)
            print("Attempting to refresh config from {}".format(config_url))
            try:
                r = requests.get(config_url)
                new_config = r.json()
                write_config_to_disk(cfg_type, new_config)
                self.debug("New config read and updated for nodule {}".format(self.UID))
            except:
                self.log_error("Could not update new config for nodule {}".format(self.UID))
        return

    def start_mqtt(self):
        self.client.user_data_set(self)
        self.client.on_connect = self.on_connect
        def presence_msg(connected=True):
            return dumps({'presence': 'Connected' if connected else 'Disconnected', 'node': self.UID})
        # LastWill must be set before connect()
        presence_channel = self.channel_mgr.presence()
        self.client.will_set(presence_channel, presence_msg(False), 0, False)
        mqtt_conf = self.config['hardware']['mqtt']
        print(mqtt_conf['mqtt_url'], mqtt_conf['mqtt_port'], mqtt_conf['mqtt_keepalive'])
        self.client.connect(mqtt_conf['mqtt_url'], mqtt_conf['mqtt_port'], mqtt_conf['mqtt_keepalive'])
        self.client.loop_start()
        self.client.publish(presence_channel, presence_msg(True))
        return

    def disconnect(self):
        """Disconnects safely, but doesn't send LWT msg"""
        print("Safely disconnecting")
        self.client.disconnect()

    # def load_in_jobs(self):
    #     """Read in list of starting jobs from file on device. Run when node
    #     first starts up. Useful in case of power loss"""
    #     if self.config['schedule']['error_reporting']['enable']:
    #         error_reporter = InternalJob(self.config['schedule']['error_reporting']['period'], self, "error_reporter", self.report_errors)
    #         self.jobs.add_job(error_reporter)
    #     if self.config['schedule']['log_reporting']['enable']:
    #         log_reporter = InternalJob(self.config['schedule']['log_reporting']['period'], self, "log_reporter", self.report_logs)
    #         self.jobs.add_job(log_reporter)
    #     return

    def backup_to_disk(self):
        """Save state of all jobs and sensors to file on device. Run when
        changes are made, so state can be restored with load_in_jobs"""
        return

    def on_connect(self, client, userdata, flags, rc):
        """Subscribing in on_connect() means that if we lose the connection and
        reconnect then subscriptions will be renewed."""
        print("Nodule '{UID}' connected with result code {rc}".format(UID=self.UID, rc=rc))
        action2cb = {"add": cb_add_job,
                    "del": cb_del_job,
                    # "show": cb_show_jobs,
                    "trigger": cb_trigger_job,   # WILL NEED TO BE ABLE TO TRIGGER JOB/ACTUATOR IMMEDIATELY BASED ON CENTRAL RULES ENGINE
                    "refresh_config": cb_refresh_config,
                    "get_logs": cb_report_logs,}
                    # "query_sensor": cb_query_sensor,}
                    # "get_errors": cb_show_errors,
                    # "report": cb_report_in,}
        for action, cb in action2cb.items():
            job_topic = "nodule/{}/{}/#".format(self.UID, action)
            # job_topic = self.channel_mgr.jobs(action)
            client.message_callback_add(job_topic, cb)
            client.subscribe(job_topic)  # Add, modify, remove, trigger, etc


def cb_refresh_config(client, userdata, msg):
    return
def cb_report_in(client, userdata, msg):
    return
def cb_add_job(client, userdata, msg):
    return
def cb_del_job(client, userdata, msg):
    return
def cb_report_logs(client, userdata, msg):
    """Return internal stats to base station"""
    return
def cb_show_jobs(client, userdata, msg):
    return
def cb_trigger_job(client, userdata, msg):
    return


# def validate_msg_fields_valid(payload):
#     fields = "name period sensor_type pin".split(' ')
#     missing_fields = [x for x in fields if x not in list(payload.keys())]
#     if len(missing_fields)>0:
#         raise Exception("The following fields are missing: " + str(missing_fields))
#     return True



if __name__ == '__main__':
    myNodule = Nodule()
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            # myNodule.disconnect()  # Explictly disconnecting doesn't send LWT, so we'll ignore this
            break
    exit(0)
