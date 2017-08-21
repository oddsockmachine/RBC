from random import randint

def get_sensor_class(sensor_type):
    sensors = {
        "DHT_11": DHT_Sensor,
        "Mock": Mock_Sensor,
    }
    return sensors.get(sensor_type)


class Sensor(object):
    """Representation of a particular type of sensor on a pin/port."""
    def __init__(self, uid, pin, name):
        super(Sensor, self).__init__()
        self.uid = uid
        self.pin = pin
        self.name = name
        self.type = "Default"
        self.units = "None"
    def report(self):
        return {'uid': self.uid, 'pin': self.pin, 'name': self.name, 'type': self.type}
    def read(self):
        raise Exception("Read function not implemented")
        return 0

class DHT_Sensor(Sensor):
    """docstring for DHT_Sensor."""
    def __init__(self, uid, pin, name):
        super(Sensor, self).__init__()
        self.uid = uid
        self.pin = pin
        self.name = name
        self.type = "DHT_11"
        self.units = "C/%"
        class DHT(object):
            def __init__(self, foo):
                self.foo = foo
            def get(self):
                return randint(0,100)
        self.randomizer = DHT(self.pin)

    def read(self):
        result_t = self.randomizer.get()
        result_h = self.randomizer.get()
        return {'temp': result_t, 'hmdy': result_h}

class Mock_Sensor(Sensor):
    """docstring for Mock_Sensor."""
    def __init__(self, uid, pin, name):
        super(Sensor, self).__init__()
        self.uid = uid
        self.pin = pin
        self.name = name
        self.type = "Fake"
        self.units = "Nothings"
        class Randomizer(object):
            def __init__(self, foo):
                self.foo = foo
            def get(self):
                return randint(0,100)
        self.randomizer = Randomizer(self.pin)

    def read(self):
        result = self.randomizer.get()
        return {'mock': {'value': result, 'units': self.units}}
