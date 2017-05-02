from random import randint
from json import dumps

client = None

def job_to_channel(location, _id):
    return "sensors/{location}/{_id}/temperature".format(location, _id)

class JobList(object):
    """docstring for JobList."""
    def __init__(self, _client):
        super(JobList, self).__init__()
        self.client = _client
        global client
        client = _client
        self.jobs = []
    def add_job(self, job):
        self.jobs.append(job)
    def get_job(self, query):
        return

class Job(object):
    """docstring for Job."""
    def __init__(self, name, period, func):
        super(Job, self).__init__()
        self.name = name
        self.period = period
        self.func = func
        self.client = client
    def execute(self):
        return self.func(args)


def report_temp(_id):
    print("Reporting temp")
    temp = randint(0,35)
    global client
    client.publish("topic", "hello"+_id)
    client.publish("topic", dumps({'ID': _id, 'temp': temp}))
    # print(schedule.jobs)
    # print(schedule.next_run())
    return temp

def report_humidity(_id):
    print("Reporting hmdy")
    hmdy = randint(0,35)
    global client
    client.publish("topic", "hello"+_id)
    client.publish("topic", dumps({'ID': _id, 'hmdy': hmdy}))
    # print(schedule.jobs)
    # print(schedule.next_run())
    return hmdy

sched = {
    report_temp: 5,
    report_humidity: 10
}

jobs = []
jobs.append(Job("report_temp", 5, report_temp))
jobs.append(Job("report_humidity", 10, report_humidity))

def get_all_jobs():
    return jobs
