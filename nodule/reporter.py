from collections import deque
from contextlib import contextmanager
from datetime import datetime
from json import dumps
from time import sleep

# """Internal buffer to queue up any reports that can't be delivered due to connectivity problems"""
class Reporter(object):
    """docstring for Reporter."""
    def __init__(self, nodule):
        super(Reporter, self).__init__()
        self.nodule = nodule
        self.client = nodule.client
        self.channels = nodule.channel_mgr
    def publish(self, msg_data):
        channel = self.channels.sensors("report", msg_data['component_uid'])
        result = self.client.publish(channel, dumps(msg_data), qos=2)
        return
    def debug(self, msg_data):
        print(msg_data)
        return
    def log_error(self, msg_data):
        print(msg_data)
        return
        # self.error_log = deque([], self.config['err_log_size'])
        # self.logs = deque([], self.config['log_size'])


@contextmanager
def log_catch(node):
    try:
        yield
    except Exception as e:
        print(e)
        msg = dumps({'timestamp': str(datetime.now()), 'error': str(e), 'node': node.name})
        node.log_error(msg)
        pass


# separate streams/channels for debug, errors, logs, reports etc.
