import paho.mqtt.client as mqtt
from jobs import JobList, Job
from functions import *
import schedule


class Node(object):
    """docstring for Node."""
    def __init__(self, name):
        super(Node, self).__init__()
        self.name = name
        self.client = mqtt.Client()
        self.jobs = JobList(self.client)
        # js = [report_temp, report_humidity]
        # jx =
        self.jobs.add_job(Job("report_temp", 5, report_temp))
        self.jobs.add_job(Job("report_humidity", 10, report_humidity))

        for j in self.jobs.all_jobs():
            schedule.every(j.period).seconds.do(j.func, "123", self.client).tag(j.name,'temp', 'sensor')

    def start(self):
        self.client.connect("127.0.0.1", 1883, 60)
        self.client.loop_start()

    def load_in_jobs(self):
        return
