from random import randint

def get_sensor_class(sensor_type):
    sensors = {
        "DHT_11": DHT_Sensor,
        "Mock": Mock_Sensor,
        "RPi_CPU_Temp": RPi_CPU_Temp,
        "RPi_Disk_Usage": RPi_Disk_Usage,
        "RPi_Mem_Usage": RPi_Mem_Usage,
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


class RPi_CPU_Temp(Sensor):
    """docstring for RPi_CPU_Temp."""
    def __init__(self, uid, pin, name):
        super(Sensor, self).__init__()
        self.uid = uid
        self.pin = pin
        self.name = name
        self.type = "CPU_Temp"
        self.units = "C"
        from subprocess import check_output
        def get_cpu_temp():
            output = check_output("vcgencmd measure_temp".split())
            output = output.decode().strip().split('=')[~0].replace("'C","")
            return output
        self.get_cpu_temp = get_cpu_temp

    def read(self):
        result = self.get_cpu_temp()
        return {'cpu_temp': {'value': result, 'units': self.units}}

class RPi_Disk_Usage(Sensor):
    """docstring for RPi_Disk_Usage."""
    def __init__(self, uid, pin, name):
        super(Sensor, self).__init__()
        self.uid = uid
        self.pin = pin
        self.name = name
        self.type = "Disk_Usage"
        self.units = "GB"
        from subprocess import check_output
        def get_disk_usage():
            output = check_output("df -h".split())
            output = output.decode().split('\n')[1]
            return output
        self.get_disk_usage = get_disk_usage

    def read(self):
        result = self.get_disk_usage()
        fs, total, used, avail, percent, mount = [r for r in result.split(' ') if len(r)>0]
        return {'disk_usage': {'total': total, 'used':used, 'available':avail, 'percent':percent, 'units': self.units}}

class RPi_Mem_Usage(Sensor):
    """docstring for RPi_Mem_Usage."""
    def __init__(self, uid, pin, name):
        super(Sensor, self).__init__()
        self.uid = uid
        self.pin = pin
        self.name = name
        self.type = "Mem_Usage"
        self.units = "GB"
        from subprocess import check_output
        def get_disk_usage():
            output = check_output("free -h".split())
            output = output.decode().split('\n')[1]
            return output
        self.get_disk_usage = get_disk_usage

    def read(self):
        result = self.get_disk_usage()
        mem, total, used, free, shared, buffers, cached = [r for r in result.split(' ') if len(r)>0]
        return {'disk_usage': {'total': total, 'used':used, 'free':free, 'units': self.units}}


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
