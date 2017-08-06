
class Sensor(object):
    """Representation of a particular type of sensor on a pin/port."""
    def __init__(self, arg):
        super(Sensor, self).__init__()
        self.arg = arg
        self.pin = 99
    def read(self):
        return 0

class DHT_Sensor(Sensor):
    """docstring for DHT_Sensor."""
    def __init__(self, arg):
        super(DHT_Sensor, self).__init__()
        self.arg = arg

class Mock_Sensor(Sensor):
    """docstring for DHT_Sensor."""
    def __init__(self, arg):
        super(DHT_Sensor, self).__init__()
        self.arg = arg


class SensorSet(object):
    """Set of sensors on all pins/ports of a Node."""
    def __init__(self):
        super(SensorSet, self).__init__()
        self.sensors = []
        self.valid_pins = [0,1,2,3,4,5]
    def get_sensor_for_pin(pin):
        return
    def get_sensor_by_id(ID):
        return
    def add_sensor(sensor):
        return
    def delete_sensor_by_id(sensor):
        return
    def delete_sensor_by_pin(sensor):
        return
