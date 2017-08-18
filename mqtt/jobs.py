from functions import *
import schedule
from json import dumps
from logger import log_catch

def job_to_channel(location, _id):
    return "sensors/{location}/{_id}/temperature".format(location, _id)

class JobList(object):
    """docstring for JobList."""
    def __init__(self, _client):
        super(JobList, self).__init__()
        self.client = _client
        # global client
        # client = _client
        self.jobs = []
    def add_job(self, job):
        self.jobs.append(job)
        # schedule.every(job.period).seconds.do(job.func, self.client, job.args).tag(job.name, job.uid, 'temp', 'sensor')
        schedule.every(job.period).seconds.do(job.execute).tag(job.name, job.uid)
        # schedule.every(job.period).seconds.do(job.func, "123", self.client).tag(job.name, 'temp', 'sensor')
    def get_job(self, query):
        return
    def all_jobs(self):
        return self.jobs
    def report_jobs(self):
        jobs = [j.__dict__.copy() for j in self.jobs]
        [j.pop("func") for j in jobs]  # Magic side effect, don't care about return value
        return jobs

class Job(object):
    """docstring for Job."""
    def __init__(self, period, node, name, func):
        super(Job, self).__init__()
        self.name = name
        self.period = period
    def default_msg(self):
        return {"node": self.node.name, "timestamp": str(datetime.now())}
    def execute(self):
        raise Exception("Execute function not implemented for {}".format(str(self)))

class SensorJob(Job):
    """docstring for Job."""
    def __init__(self, period, node, sensor):
        # super(SensorJob, self).__init__()
        self.name = sensor.name
        self.period = int(period)
        self.sensor = sensor
        self.uid = sensor.uid
        self.last_run = None  # TODO keep track of last run time on file
        self.client = node.client
        self.node = node
    def execute(self):
        with log_catch(self.node):
            result = self.sensor.read()
            msg = self.default_msg()
            channel = self.node.channel.sensors(self.node.name, self.sensor.type, self.name)
            msg.update({"job_id": self.uid, "job_name":self.name, "pin": self.sensor.pin, "type": self.sensor.type, "value": str(result)})
            self.client.publish(channel, dumps(msg))
            self.last_run = datetime.now()

class InternalJob(Job):
    """docstring for Job."""
    def __init__(self, period, node, name, func):
        # super(InternalJob, self).__init__()
        self.period = int(period)
        self.name = name
        self.uid = "error_reporter"
        self.last_run = None  # TODO keep track of last run time on file
        self.client = node.client
        self.node = node
        self.func = func
    def execute(self):
        with log_catch(self.node):
            self.last_run = datetime.now()
            return self.func()
