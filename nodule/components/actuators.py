from random import randint
# import RPi.GPIO as GPIO
# import dht11
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.cleanup()

def get_actuator_class(actuator_type):
    actuators = {
        "relay": Relay,
        "pump": Pump,
        "servo": Servo,
    }
    return actuators.get(actuator_type)




class Actuator(object):
    """Representation of a particular type of actuator on a pin/port."""
    def __init__(self, uid, pin_num, description):
        super(Actuator, self).__init__()
        self.uid = uid
        self.pin_num = pin_num
        self.pin = None
        self.description = description
        self.type = "Default"
        self.required_params = []
    # def report(self):
    #     return {'uid': self.uid, 'pin': self.pin, 'description': self.description, 'type': self.type}
    def validate_params(params):
        for p in params:
            if p not in self.required_params:
                raise Exception("Parameter {} not provided when calling {}".format(p, self.description))
        return
    def actuate(self, params):
        raise Exception("Actuate function not implemented")
        return
    def call(self, params):
        self.validate_params(params)
        self.call(params)
        return

class Relay(Actuator):
    """Representation of a particular type of actuator on a pin/port."""
    def __init__(self, uid, pin_num, description):
        super(Actuator, self).__init__()
        self.uid = uid
        self.pin_num = pin_num
        # self.pin = machine.Pin(pin_num, machine.Pin.OUT, machine.Pin.PULL_UP)
        self.description = description
        self.type = "Relay"
    def actuate(self, parameters):
        on_time = parameters['on_time']
        self.pin.on()
        sleep(on_time)
        self.pin.off()
        return

class Pump(Actuator):
    """Representation of a particular type of actuator on a pin/port."""
    def __init__(self, uid, pin_num, description):
        super(Actuator, self).__init__()
        self.uid = uid
        self.pin_num = pin_num
        # self.pin = machine.Pin(pin_num, machine.Pin.OUT, machine.Pin.PULL_UP)
        self.description = description
        self.type = "Pump"
        self.required_params = ['on_time', 'dispense_amount']
    def actuate(self, parameters):
        on_time = parameters['on_time']
        dispense_amount = parameters['dispense_amount']
        self.pin.on()
        sleep(on_time)
        self.pin.off()
        return

class Servo(Actuator):
    """Representation of a particular type of actuator on a pin/port."""
    def __init__(self, uid, pin_num, description):
        super(Actuator, self).__init__()
        self.uid = uid
        self.pin_num = pin_num
        # self.pin = machine.Pin(pin_num, machine.Pin.OUT, machine.Pin.PULL_UP)
        self.description = description
        self.type = "Servo"
        self.required_params = ['end_position', 'move_time']
    def actuate(self, parameters):
        end_position = parameters['end_position']
        move_time = parameters['move_time']
        # self.pin.on()
        # sleep(on_time)
        # self.pin.off()
        return


class Mock_Actuator(Actuator):
    """Representation of a particular type of actuator on a pin/port."""
    def __init__(self, uid, pin_num, description):
        super(Actuator, self).__init__()
        self.uid = uid
        self.pin_num = pin_num
        # self.pin = machine.Pin(pin_num, machine.Pin.OUT, machine.Pin.PULL_UP)
        self.description = description
        self.type = "Mock_Actuator"
        self.required_params = ['param1', 'param2']
    def actuate(self, parameters):
        param1 = parameters['param1']
        param2 = parameters['param2']
        # self.pin.on()
        # sleep(on_time)
        # self.pin.off()
        return
