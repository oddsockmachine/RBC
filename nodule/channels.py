# Define channel names here


class ChannelMgr(object):
    """Helper functions to manage channel urls"""
    def __init__(self, node_uid):
        super(ChannelMgr, self).__init__()
        self.node_uid = node_uid

    def presence(self):
        return "presence/{node_uid}".format(node_uid=self.node_uid)

    def errors(self):
        return "errors/{node_uid}".format(node_uid=self.node_uid)

    def logs(self):
        return "logs/{node_uid}".format(node_uid=self.node_uid)

    def report(self):
        return "report/{node_uid}".format(node_uid=self.node_uid)

    def actuators(self, action, actuator_uid):
        # action should be trigger or report
        return "actuators/{action}/{node_uid}/{actuator_uid}".format(action=action, node_uid=self.node_uid, actuator_uid=actuator_uid)

    def sensors(self, action, sensor_uid):
        # action should be trigger or report
        return "sensors/{action}/{node_uid}/{sensor_uid}".format(action=action, node_uid=self.node_uid, sensor_uid=sensor_uid)
