from random import randint
import glob
import socket
from subprocess import check_output

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
        "ds18b20": DS18B20_Sensor,
        "moisture": Mock_Sensor,
        "TSL2561": Mock_Sensor,
        "OPI_stats": OPI_Stats_Sensor,
        "IP": IP_Sensor,
        "uptime": Uptime_Sensor,
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



class DS18B20_Sensor(Sensor):
    """docstring for DS18B20_Sensor."""
    def __init__(self, uid, pin_num, description):
        super(Sensor, self).__init__()
        print("creating ds18b20")
        self.uid = uid
        self.pin_num = pin_num
        self.description = description
        self.type = "ds18b20"
        self.units = "C"
        print("created")

    def read(self):
        # print("reading ds18b20")
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
        def read_temp_raw():
            f = open(device_file, 'r')
            lines = f.readlines()
            f.close()
            return lines
        def read_temp():
            lines = read_temp_raw()
            if lines[0].strip()[-3:] != 'YES':
                return {'temp': 'error'}
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                # print(temp_c)
                return {'temp': temp_c}
            return {'temp': 'error'}
        return read_temp()




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

class OPI_Stats_Sensor(Sensor):
    """docstring for Stats_Sensor."""
    def __init__(self, uid, pin_num, description):
        super(Sensor, self).__init__()
        print("creating ds18b20")
        self.uid = uid
        self.pin_num = pin_num
        self.description = description
        self.type = "ds18b20"
        self.units = "C"
        print("created")

    def read(self):
        # TODO
        cmd = 'sudo armbianmonitor -m'

class IP_Sensor(Sensor):
    """docstring for IP_Sensor."""
    def __init__(self, uid, pin_num, description):
        super(Sensor, self).__init__()
        print("creating IP sensor")
        self.uid = uid
        self.description = description
        self.type = "ip_address"
        print("created")

    def read(self):
        # print("Getting IP")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        # print(IP)
        return  {'IP': {'value': IP}}


class Uptime_Sensor(Sensor):
    """docstring for Uptime_Sensor."""
    def __init__(self, uid, pin_num, description):
        super(Sensor, self).__init__()
        self.uid = uid
        self.description = description
        self.type = "uptime"

    def read(self):
        # print("Getting uptime")
        uptime = str(check_output(["uptime"]))
        uptime = uptime[12:-3].split('user')[0].split(',')[0]
        print(uptime)
        return  {'uptime': {'value': uptime}}
