from components.sensors import get_sensor_class
from components.actuators import get_actuator_class

class GPIO_Set(object):
    """Set of sensors and actuators on all pins/ports of a Node."""
    def __init__(self, nodule):
        super(GPIO_Set, self).__init__()
        self.nodule = nodule
        self.sensors = []
        self.actuators = []
        hw_type = nodule.config['nodule']['HW_TYPE']
        self.valid_pins = nodule.config['hardware']['valid_pins'][hw_type]  # TODO get from config based on hardware type
        self.used_pins = set()
        self.load_sensors_from_config(nodule.config['sensors'])
        self.load_actuators_from_config(nodule.config['actuators'])
        print(self.get_component_by_attr('sensor', 'uid', 'xyz444').description)
        print(self.get_component_by_attr('sensor', 'pin_num', 'i2c_3').description)

    def get_component_by_attr(self, kind, attr, value):
        group = self.sensors if kind == "sensor" else self.actuators
        x = [x for x in group if x.__dict__.get(attr) == value]
        if len(x) == 1:
            return x[0]
        if len(x) == 0:
            raise Exception("{}: {} not found".format(kind, uid))
        return

    def load_sensors_from_config(self, sensor_config):
        for new_sens_cfg in sensor_config:
            sensor_class = get_sensor_class(new_sens_cfg['type'])
            uid = new_sens_cfg['uid']
            pin_num = new_sens_cfg['pin']
            description = new_sens_cfg['description']
            new_sensor = sensor_class(uid, pin_num, description)
            self.sensors.append(new_sensor)
            self.used_pins.add(pin_num)
        return

    def load_actuators_from_config(self, actuator_config):
        for new_actuator_cfg in actuator_config:
            actuator_class = get_actuator_class(new_actuator_cfg['type'])
            uid = new_actuator_cfg['uid']
            pin_num = new_actuator_cfg['pin']
            description = new_actuator_cfg['description']
            new_actuator = actuator_class(uid, pin_num, description)
            self.actuators.append(new_actuator)
            self.used_pins.add(pin_num)
        return

    def report(self):
        return {'sensors': {s.name: s.pin for s in self.sensors}, 'used_pins': self.used_pins, 'valid_pins': self.valid_pins}


# if __name__ == '__main__':
    # from random import randint
    # sensor_set = GPIO_Set()
    # sensorA = Mock_Sensor('123', 1, 'sensorA')
    # sensorB = Mock_Sensor('456', 2, 'sensorB')
    # sensorC = Mock_Sensor('789', 1, 'sensorC')
    # sensorD = Mock_Sensor('456', 3, 'sensorD')
    #
    # sensor_set.add_sensor(sensorA)
    # sensor_set.add_sensor(sensorB)
    # try:
    #     sensor_set.add_sensor(sensorC)
    # except:
    #     pass
    # try:
    #     sensor_set.add_sensor(sensorD)
    # except:
    #     pass
    #
    # sensorX = sensor_set.get_sensor_by_id('456')
    # print(sensorX.name)
    # sensorY = sensor_set.get_sensor_by_pin(1)
    # print(sensorY.name)
    # print(sensorX.read())
