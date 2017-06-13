from functions import *
import schedule

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
        schedule.every(job.period).seconds.do(job.func, self.client, job.args).tag(job.name, job.uid, 'temp', 'sensor')
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
    def __init__(self, name, period, func, args):
        super(Job, self).__init__()
        self.name = name
        self.period = period
        self.func = func
        self.pin = args.get('pin')
        self.uid = self.name + '_' + self.pin
        # self.client = client
        self.args = args  # args for eg pin numbers, multipliers etc
        self.args['job_uid'] = self.uid
    def execute(self):
        return self.func(args)
