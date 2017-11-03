
class SensorSet(object):
    """Set of sensors on all pins/ports of a Node."""
    def __init__(self):
        super(SensorSet, self).__init__()
        self.sensors = []
        self.valid_pins = [0,1,2,3,4,5]  # TODO get from config based on hardware type
        self.used_pins = []

    def report(self):
        return {'sensors': {s.name: s.pin for s in self.sensors}, 'used_pins': self.used_pins, 'valid_pins': self.valid_pins}

    def get_sensor_by_pin(self, pin):
        s = [s for s in self.sensors if s.pin == pin]
        if len(s) == 1:
            return s[0]
        if len(s) == 0:
            raise Exception("Sensor not found")
            return None
        else:
            raise Exception("Conflicting sensor pins found")
            return None
        return

    def get_sensor_by_id(self, ID):
        s = [s for s in self.sensors if s.uid == ID]
        if len(s) == 1:
            return s[0]
        if len(s) == 0:
            raise Exception("Sensor not found")
            return None
        else:
            raise Exception("Conflicting sensor UIDs found")
            return None
        return

    def add_sensor(self, sensor):
        if sensor.pin in self.used_pins:
            conflict = self.get_sensor_by_pin(sensor.pin)
            raise Exception("Error: Pin {} already in use by {}".format(conflict.pin, conflict.name))
            return None
        if sensor.uid in [s.uid for s in self.sensors]:
            conflict = self.get_sensor_by_id(sensor.uid)
            raise Exception("Error: UID {} already in use by {}".format(conflict.uid, conflict.name))
            return None
        self.used_pins.append(sensor.pin)
        self.sensors.append(sensor)
        return

    def delete_sensor_by_id(self, sensor):
        return

    def delete_sensor_by_pin(self, sensor):
        return

# if __name__ == '__main__':
    # from random import randint
    # sensor_set = SensorSet()
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
