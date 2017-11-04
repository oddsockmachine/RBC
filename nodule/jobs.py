from functions import *
import schedule
from json import dumps
from logger import log_catch

# def job_to_channel(location, _id):
#     return "sensors/{location}/{_id}/temperature".format(location, _id)

class JobList(object):
    """docstring for JobList."""
    def __init__(self, nodule):
        super(JobList, self).__init__()
        self.nodule = nodule
        self.jobs = []
        self.load_jobs_from_config(nodule.config['jobs'])


    def load_jobs_from_config(self, job_configs):
        from pprint import pprint
        pprint(job_configs)
        for new_job_config in job_configs:
            job_type = new_job_config['type']
            if job_type in ['sensor', 'actuator']:
                component = self.nodule.gpio_set.get_component_by_attr(job_type, 'uid', new_job_config['component'])
                print(new_job_config['description'], component.description)
                new_job = Job(new_job_config['period'], self.nodule, new_job_config['uid'], component, new_job_config['type'])
                self.add_job(new_job)
        return

    def add_job(self, job):
        self.jobs.append(job)
        # schedule.every(job.period).seconds.do(job.func, self.client, job.args).tag(job.name, job.uid, 'temp', 'sensor')
        schedule.every(job.period).seconds.do(job.call).tag(job.kind, job.uid)
        # schedule.every(job.period).seconds.do(job.func, "123", self.client).tag(job.name, 'temp', 'sensor')
    def get_job(self, query):
        return
    def all_jobs(self):
        return [j.report() for j in self.jobs]
    def report_jobs(self):
        jobs = [j.__dict__.copy() for j in self.jobs]
        [j.pop("func") for j in jobs]  # Magic side effect, don't care about return value
        return jobs

class Job(object):
    """docstring for Job."""
    def __init__(self, period, nodule, uid, component, kind):
        super(Job, self).__init__()
        self.uid = uid
        self.period = period
        self.kind = kind
        self.component = component
    def call(self):
        msg = self.execute()
        msg.update(self.default_msg())
        self.report(msg)
    def default_msg(self):
        """Provide default data that should be sent with each message"""
        return {"job_uid": self.uid, "component_uid": self.component.uid, "timestamp": str(datetime.now())}
    def execute(self):
        return {"values": "999"}
        raise Exception("Execute function not implemented for {}".format(str(self)))
    def report(self, msg):
        """Wrap message from sensor, actuator etc and send to reporter"""
        print(msg)
        return
        return {'uid': self.uid, 'type': self.__class__.__name__}

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
    def report(self):
        x = {'name': self.name, 'type': self.__class__.__name__, 'period': self.period, 'sensor': self.sensor.report(), 'uid': self.uid, 'last_run': str(self.last_run), 'node': self.node.name}
        return x

    def execute(self):
        with log_catch(self.node):
            result = self.sensor.read()
            msg = self.default_msg()
            channel = self.node.channel.sensors(self.node.name, self.sensor.type, self.name)
            msg.update({"job_id": self.uid, "job_name":self.name, "pin": self.sensor.pin, "type": self.sensor.type, "value": str(result)})
            self.client.publish(channel, dumps(msg))
            self.last_run = datetime.now()

class ActuatorJob(Job):
    """docstring for ActuatorJob."""
    def __init__(self, period, node, sensor):
        return

class InternalJob(Job):
    """docstring for Job."""
    def __init__(self, period, node, name, func):
        # super(InternalJob, self).__init__()
        self.period = int(period)
        self.name = name
        self.uid = "~".join([node.name, "internal", name])
        self.last_run = None  # TODO keep track of last run time on file
        self.client = node.client
        self.node = node
        self.func = func
    def report(self):
        return {'name': self.name, 'type': self.__class__.__name__, 'period': self.period, 'func': self.func.__name__, 'uid': self.uid, 'last_run': str(self.last_run), 'node': self.node.name}
    def execute(self):
        with log_catch(self.node):
            self.last_run = datetime.now()
            return self.func()
