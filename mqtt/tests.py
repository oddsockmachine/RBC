import unittest
from sensors import *


class TestSensorMethods(unittest.TestCase):

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')
    #
    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

    def test_basic_add(self):
        sensor_set = SensorSet()
        sensorA = Sensor('123', 1, lambda x:1, 'sensorA')
        sensorB = Sensor('456', 2, lambda x:1, 'sensorB')

    def test_error_conditions(self):
        sensor_set = SensorSet()
        sensorA = Sensor('123', 1, lambda x:1, 'sensorA')
        sensorB = Sensor('456', 2, lambda x:1, 'sensorB')
        with self.assertRaises(Exception):
            sensorC = Sensor('789', 1, lambda x:1, 'sensorC')
        with self.assertRaises(Exception):
            sensorD = Sensor('456', 3, lambda x:1, 'sensorD')



if __name__ == '__main__':
    unittest.main()


    sensor_set = SensorSet()
    sensorA = Sensor('123', 1, lambda x:1, 'sensorA')
    sensorB = Sensor('456', 2, lambda x:1, 'sensorB')
    sensorC = Sensor('789', 1, lambda x:1, 'sensorC')
    sensorD = Sensor('456', 3, lambda x:1, 'sensorD')

    sensor_set.add_sensor(sensorA)
    sensor_set.add_sensor(sensorB)
    sensor_set.add_sensor(sensorC)
    sensor_set.add_sensor(sensorD)

    sensorX = sensor_set.get_sensor_by_id('456')
    print(sensorX.name)
    sensorY = sensor_set.get_sensor_by_pin(1)
    print(sensorY.name)
