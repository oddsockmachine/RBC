from random import randint
# import RPi.GPIO as GPIO
# import dht11
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.cleanup()

def get_sensor_class(sensor_type):
    sensors = {
        # "DHT_11": DHT_Sensor,
        "DHT_11": Mock_Sensor,
        "Mock": Mock_Sensor,
        "DS_temp": Mock_Sensor,
        "LDR": Mock_Sensor,
        # "RPi_CPU_Temp": RPi_CPU_Temp,
        # "RPi_Disk_Usage": RPi_Disk_Usage,
        # "RPi_Mem_Usage": RPi_Mem_Usage,
    }
    return sensors.get(sensor_type)


class Sensor(object):
    """Representation of a particular type of sensor on a pin/port."""
    def __init__(self, uid, pin_num, description):
        super(Sensor, self).__init__()
        self.uid = uid
        self.pin_num = pin_num
        # self.pin = machine.Pin(pin_num, machine.Pin.OUT, machine.Pin.PULL_UP)
        self.description = description
        self.type = "Default"
        self.units = "None"
    def report(self):
        return {'uid': self.uid, 'pin': self.pin, 'description': self.description, 'type': self.type}
    def read(self):
        raise Exception("Read function not implemented")
        return 0
    def sense(self):
        return




class DHT_Sensor(Sensor):
    """docstring for DHT_Sensor."""
    def __init__(self, uid, pin_num, description):
        super(Sensor, self).__init__()
        self.uid = uid
        self.pin_num = pin_num
        self.description = description
        self.type = "DHT_11"
        self.units = "C/%"
        self.dht11_instance = dht11.DHT11(pin=int(self.pin_num))

    def read(self):
        attempts = 0
        result = self.dht11_instance.read()
        while not result.is_valid() and attempts < 5:
            result = self.dht11_instance.read()
        if not result.is_valid():
            raise("Error reading from "+ self)
        result_t = result.temperature
        result_h = result.humidity
        return {'temp': result_t, 'hmdy': result_h}



class Mock_Sensor(Sensor):
    """docstring for Mock_Sensor."""
    def __init__(self, uid, pin_num, description):
        super(Sensor, self).__init__()
        self.uid = uid
        self.pin_num = pin_num
        self.description = description
        self.type = "Fake"
        self.units = "Nothings"
        class Randomizer(object):
            def __init__(self, foo):
                self.foo = foo
            def get(self):
                return randint(0,100)
        self.randomizer = Randomizer(self.pin_num)

    def read(self):
        result = self.randomizer.get()
        return {'mock': {'value': result, 'units': self.units}}
