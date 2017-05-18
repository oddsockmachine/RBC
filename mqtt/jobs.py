from functions import *
# client = None

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
    def get_job(self, query):
        return
    def all_jobs(self):
        return self.jobs

class Job(object):
    """docstring for Job."""
    def __init__(self, name, period, func):
        super(Job, self).__init__()
        self.name = name
        self.period = period
        self.func = func
        # self.client = client
        self.args = []  # args for eg pin numbers, multipliers etc
    def execute(self):
        return self.func(args)



sched = {
    report_temp: 5,
    report_humidity: 10
}

# jobs = []
# jobs.append(Job("report_temp", 5, report_temp))
# jobs.append(Job("report_humidity", 10, report_humidity))
#
# def get_all_jobs():
#     return jobs
#
