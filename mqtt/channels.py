# Define channel names here


class ChannelMgr(object):
    """Helper functions to manage channel urls"""
    def __init__(self, nodename):
        super(ChannelMgr, self).__init__()
        self.nodename = nodename


    def jobs(self, command):
        return "jobs/{nodename}/{command}/#".format(nodename=self.nodename, command=command)

    def errors(self):
        return "errors/{nodename}".format(nodename=self.nodename)

    def logs(self):
        return "logs/{nodename}".format(nodename=self.nodename)

    def presence(self):
        return "presence/{nodename}".format(nodename=self.nodename)

    def actions(self, actuator, action):
        return "actions/{nodename}/{actuator}/{action}/#".format(nodename=self.nodename, actuator=actuator, action=action)

    def sensors(self, node, sensor_type, uid):
        return "sensors/{nodename}/{sensor_type}/{uid}".format(nodename=self.nodename, sensor_type=sensor_type, uid=uid)
